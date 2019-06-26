#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.globalvar import global_const
import importlib
import os

class action_help(server_action):
    __parameters__ = [
        {"name":"h", "needarg":False, "desc":"显示这条帮助信息"}
    ]
    def __init__(self):
        self.__usage_helper__ = usage_helper(sys.argv[0], "help", self.__parameters__)

    def __usage__(self):
        self.__usage_helper__.output()

    def description(self):
        return "显示命令的帮助信息"

    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self.__usage_helper__.get_opt_string())
        except Exception as e:
            self.__usage__()
            exit()
        for opt,arg in opts:
            if opt == '-h':
                self.__usage__()
                exit()

    def run(self):
        search_dir = "%s/core/action"%(global_const().get_value('BASEDIR'))
        cmd_array=[]
        for file in os.listdir(search_dir):
            filename,extname = os.path.splitext(file)
            if extname == ".py":
                m = importlib.import_module("core.action."+filename)
                try:
                    class_func = getattr(m, "action_" + filename)
                    o = class_func()
                    # 检查是否server_action类型，如果是这个类型的话，表示是一个指令
                    if o.__class__.__base__.__name__ == 'server_action':
                        cmd_info = (filename, o)
                        cmd_array.append(cmd_info)
                except Exception as e:
                    pass

        sw_name = os.path.basename(sys.argv[0])
        print("Usage: %s cmd [options]"%(sw_name))
        print("可以使用的cmd如下:")
        for cmd, cmd_obj in cmd_array:
            start_line="%s %s"%(sw_name, cmd)
            print("\t%s %s %s"%(start_line, ' '*(35 - len(start_line)), cmd_obj.description()))