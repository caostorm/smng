#coding=utf-8
import sys
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.parser import config_parser
import getopt
import os

class action_login(server_action):
    _parameters = [
        {"name":"i", "desc":"要登录的服务器ip，这个ip必须在软件管理列表内", "needarg":True, "argname":"ip"},
        {"name":"h", "desc":"显示这条帮助信息", "needarg":False}
    ]

    def __init__(self):
        self._usage_helper = usage_helper(sys.argv[0], "login", self._parameters)

    def _usage(self):
        self._usage_helper.output()

    def description(self):
        return "使用记录列表内的服务器信息登录指定的服务器"

    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self._usage_helper.get_opt_string())
        except Exception as e:
            self._usage()
            exit()
        for opt,arg in opts:
            if opt == '-i':
                self._ip = arg
            elif opt == '-h':
                self._usage()
                exit()

    def run(self):
        parser = config_parser()
        server_info = parser.get_record(self._ip)
        os.system("general %s %s %s \"%s\""%(server_info['ip'], server_info['port'], server_info['user'], server_info['password']))
