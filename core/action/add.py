#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.parser import config_parser

class action_add(server_action):
    _parameters = [
            {"name":"u","desc":"登录服务器的用户名","needarg":True,"argname":"user"},
            {"name":"p","desc":"服务器的端口","needarg":True,"argname":"port"},
            {"name":"i","desc":"服务器的地址","needarg":True,"argname":"ip"},
            {"name":"P","desc":"登录服务器的密码","needarg":True,"argname":"password"},
            {"name":"h","desc":"显示这条帮助信息","needarg":False}
            ]
    def __init__(self):
        self._usage_helper = usage_helper(sys.argv[0], "add", self._parameters)

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

    def run(self):
        config = config_parser()
        config.add_record(self._ip, self._port, self._user, self._password)
