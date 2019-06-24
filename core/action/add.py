#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.parser import config_parser

class action_add(server_action):
    __parameters__ = [
            {"name":"u","desc":"登录服务器的用户名","needarg":True,"argname":"user"},
            {"name":"p","desc":"服务器的端口","needarg":True,"argname":"port"},
            {"name":"i","desc":"服务器的地址","needarg":True,"argname":"ip"},
            {"name":"a","desc":"登录服务器的密码","needarg":True,"argname":"password"},
            {"name":"h","desc":"显示这条帮助信息","needarg":False}
            ]
    def __init__(self):
        self.__usage_helper__ = usage_helper(sys.argv[0], "add", self.__parameters__)

    def __usage__(self):
        self.__usage_helper__.output()

    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self.__usage_helper__.get_opt_string())
        except:
            self.__usage__()
            exit()
        for opt,arg in opts:
            if opt == '-u':
                self.__user__ = arg
            elif opt == '-p':
                self.__port__ = arg
            elif opt == '-i':
                self.__ip__ = arg
            elif opt == '-a':
                self.__password__ = arg
            elif opt == '-h':
                self.__usage__()
                exit()

    def run(self):
        config = config_parser()
        config.add_record(self.__ip__, self.__port__, self.__user__, self.__password__)
