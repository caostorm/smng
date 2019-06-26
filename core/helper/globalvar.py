#coding=utf-8
import sys

# 通过单例实现全局变量的存取
class global_var(object):
    def __init__(self):
        pass

    def __new__(self, *args, **kwargs):
        if not hasattr(self, '__instance__'):
            self.__instance__ = super(global_var, self).__new__(self)
            self._global_value_ = {}
        return self.__instance__

    def set_value(self, name, value):
        self._global_value_[name] = value

    def get_value(self, name):
        try:
            return self._global_value_[name]
        except:
            return None 

# 用单例实现的伪常量，所有的值只能设置一次
class global_const(object):
    def __init__(self):
        pass

    def __new__(self, *args, **kwargs):
        if not hasattr(self, '__instance__'):
            self.__instance__ = super(global_const, self).__new__(self)
            self._global_const_ = {}
        return self.__instance__

    def _check_has_value_(self, name):
        if sys.version_info.major == 2:
            return self._global_const_.has_key(name)
        elif sys.version_info.major == 3:
            return name in self._global_const_


    def set_value(self, name, value):
        if not self._check_has_value_(name):
            self._global_const_[name] = value

    def get_value(self, name):
        try:
            return self._global_const_[name]
        except:
            return None
