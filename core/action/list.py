#coding=utf-8
import json
from core.interface.action import server_action
from core.helper.parser import config_parser
from prettytable import PrettyTable

class action_list(server_action):
    def __init__(self):
        pass

    def description(self):
        return "列出记录列表内的所有服务器ip"

    def parse_parameters(self):
        pass

    def run(self):
        disp = PrettyTable(["IP"])
        config = config_parser()
        for i in config:
            disp.add_row([i['ip']])
        print(disp)