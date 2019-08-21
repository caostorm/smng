#coding=utf-8
import sys
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.parser import config_parser
from core.helper.config import options_config
import getopt
import os

class action_login(server_action):
    _parameters = [
        {"name":"h", "desc":"显示这条帮助信息", "needarg":False},
        {"name":"i", "desc":"要登录的服务器ip，这个ip必须在软件管理列表内", "needarg":True, "argname":"ip"},
        {"name":"d", "desc":"使用系统内设置的默认参数登录", "needarg":False, "argname":"default"}
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
        self._default = False
        for opt,arg in opts:
            if opt == '-i':
                self._ip = arg
            elif opt == '-h':
                self._usage()
                exit()
            elif opt == '-d':
                self._default = True

    def _load_default_login_opts(self):
        cfg = options_config()
        username = cfg.read('default_user')
        password = cfg.read('default_password')
        port = cfg.read('default_port')
        return (username, password, port)

    def run(self):
        parser = config_parser()
        if self._default is True:
            username,password,port = self._load_default_login_opts()
        else:
            server_info = parser.get_record(self._ip)
            username = server_info['user']
            password = server_info['password']
            port = server_info['port']
        os.system("general %s %s %s \"%s\""%(self._ip, port, username, password))
