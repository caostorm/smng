#coding=utf-8
from core.interface.action import server_action
from core.helper.creator import create_action
from core.helper.globalvar import global_const
import os

class smng:
    def __init__(self):
        global_const().set_value('BASEDIR', os.path.dirname(__file__))

    def run(self):
        try:
            action = create_action()
        except:
            action = create_action('help')
        action.parse_parameters()
        action.run()
