#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.parser import config_parser
import re

class action_add(server_action):
    _parameters = [
            {"name":"u","desc":"登录服务器的用户名","needarg":True,"argname":"user"},
            {"name":"p","desc":"服务器的端口","needarg":True,"argname":"port"},
            {"name":"i","desc":"服务器的地址","needarg":True,"argname":"ip"},
            {"name":"P","desc":"登录服务器的密码","needarg":True,"argname":"password"},
            {"name":"h","desc":"显示这条帮助信息","needarg":False},
            {"name":"n", "desc": "服务器的别名", "needarg": True, "argname":"name"},
            {"name":"t", "desc": "服务器标签", "needarg": True, "argname":"tag"}
            ]
    def __init__(self):
        self._usage_helper = usage_helper(sys.argv[0], "add", self._parameters)
        self._config = config_parser()

    def _usage(self):
        self._usage_helper.output()

    def description(self):
        return "添加一条服务器信息到记录列表"

    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self._usage_helper.get_opt_string())
        except:
            self._usage()
            exit()
        self._name=None
        prog_with_value = re.compile('^[\w]+=[0-9a-zA-Z-_]+$')
        prog_without_value = re.compile('^[\w]+$')
        for opt,arg in opts:
            if opt == '-u':
                self._user = arg
            elif opt == '-p':
                self._port = arg
            elif opt == '-i':
                self._ip = arg
            elif opt == '-P':
                self._password = arg
            elif opt == '-h':
                self._usage()
                exit()
            elif opt == '-n':
                self._name = arg
            elif opt == '-t':
                if not hasattr(self, '_tag'):
                    self._tag=[]
                if prog_with_value.match(arg) is not None:
                    # 带值的标签，例如tag=hello
                    name,value = arg.split('=')
                    arg_string='%s="%s"'%(name,value)
                    self._tag.append(arg_string)
                elif prog_without_value.match(arg) is not None:
                    # 不带值的标签，例如tag
                    arg_string='%s=""'%arg
                    self._tag.append(arg_string)
                else:
                    print("%s is bad value"%(arg))
                    pass

    def _add_tag(self):
        code="self._config.add_tag(self._ip,%s)"%(','.join(self._tag))
        eval(code,globals(), locals())

    def run(self):
        self._config.add_record(self._ip, self._port, self._user, self._password, self._name)
        self._add_tag()