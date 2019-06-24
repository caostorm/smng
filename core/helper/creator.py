#coding=utf-8
import sys
from core.action.add import action_add
from core.action.list import action_list
from core.action.login import action_login

def create_action():
    action=sys.argv[1]
    class_name = "action_%s"%(action)
    obj = globals()[class_name]()
    return obj