#coding=utf-8
import sys
import importlib

def create_action(actionName = None):
    if actionName == None:
        action = sys.argv[1]
    else:
        action = actionName
    m = importlib.import_module('core.action.%s'%(action))
    class_name = "action_%s"%(action)
    class_create_function = getattr(m, class_name)
    obj = class_create_function()
    return obj