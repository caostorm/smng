#coding=utf-8
from abc import ABCMeta, abstractmethod

class server_action(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def parse_parameters(self):
        pass

    @abstractmethod
    def run(self):
        pass