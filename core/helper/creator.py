#coding=utf-8
import sys
import importlib

def create_action():
    action = sys.argv[1]
    m = importlib.import_module('core.action.%s'%(action))
    class_name = "action_%s"%(action)
    class_create_function = getattr(m, class_name)
    obj = class_create_function()
    return obj