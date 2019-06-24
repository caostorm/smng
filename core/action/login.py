#coding=utf-8
import sys
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.parser import config_parser
import getopt
import os

class action_login(server_action):
    __parameters__ = [
        {"name":"i", "desc":"要登录的服务器ip，这个ip必须在软件管理列表内", "needarg":True, "argname":"ip"},
        {"name":"h", "desc":"显示这条帮助信息", "needarg":False}
    ]

    def __init__(self):
        self.__usage_helper__ = usage_helper(sys.argv[0], "login", self.__parameters__)

    def __usage__(self):
        self.__usage_helper__.output()

    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self.__usage_helper__.get_opt_string())
        except Exception as e:
            self.__usage__()
            exit()
        for opt,arg in opts:
            if opt == '-i':
                self.__ip__ = arg
            elif opt == '-h':
                self.__usage__()
                exit()

    def run(self):
        parser = config_parser()
        server_info = parser.get_record(self.__ip__)
        os.system("general %s %s %s \"%s\""%(server_info['ip'], server_info['port'], server_info['user'], server_info['password']))
