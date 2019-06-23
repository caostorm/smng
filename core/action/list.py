import json
from core.interface.action import server_action
from core.helper.parser import config_parser

class action_list(server_action):
    def __init__(self):
        pass

    def parse_parameters(self):
        pass

    def run(self):
        config = config_parser()
        for i in config:
            print(i['ip'])