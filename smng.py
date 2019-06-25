#coding=utf-8
from core.interface.action import server_action
from core.helper.creator import create_action
from core.helper.globalvar import global_const
import os

class smng:
    def __init__(self):
        global_const().set_value('BASEDIR', os.path.dirname(__file__))

    def run(self):
        action = create_action()
        action.parse_parameters()
        action.run()
