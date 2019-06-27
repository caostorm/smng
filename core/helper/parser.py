#coding=utf-8
import json
from core.helper.crypt import pwd_crypt
from core.helper.globalvar import global_const
from copy import copy
import os

class config_parser:
    # 自定义异常，找不到对应的服务器记录
    class ErrorNotFind(BaseException):
        def __init__(self):
            pass
        
        def __str__(self):
            return 'Can not find the record'

    def __init__(self,config_path=None):
        if config_path == None:
            self._config_file_path = "%s/etc/config.json" % (global_const().get_value("BASEDIR"))
        else:
            self._config_file_path = config_path
        self._parse()

    # 从文件中读取JSON并解析出来存在成员变量内
    def _parse(self):
        with open(self._config_file_path, "a+") as f:
            try:
                f.seek(0)
                self._config = json.loads(f.read())
            except Exception as e:
                self._config = []

    # 将数据同步到文件
    def _sync(self):
        with open(self._config_file_path, "w+") as f:
            f.write(json.dumps(self._config))

    # 迭代器方法
    def __iter__(self):
        self._current = 0
        return self

    # python2 迭代器兼容
    def next(self):
        return self.__next__()

    # 迭代器方法
    def __next__(self):
        if self._config == None:
            raise StopIteration
        elif self._current < len(self._config):
            cur_record = copy(self._config[self._current])
            self._current+=1
            crypto = pwd_crypt()
            password = crypto.decrypt(cur_record['password'])
            cur_record['password'] = password
            return cur_record
        else:
            raise StopIteration

    # 添加一条服务器信息
    def add_record(self, ip, port, user, password):
        # 先查找是否有对应的ip,如果有的话则不做任何处理
        for record in self._config:
            if record['ip'] == ip:
                return
        crypto = pwd_crypt()
        obj = {"ip":ip, "port": port, "user":user, "password":crypto.encrypt(password)}
        self._config.append(obj)
        self._sync()

    # 根据ip删除一条服务器信息
    def remove_record(self, ip):
        index = None
        for record in self._config:
            if record['ip'] == ip:
                index = self._config.index(record)
        if None != index:
            del self._config[index]
        self._sync()

    # 根据ip获取一条服务器信息
    def get_record(self, ip):
        ret_record = None
        for record in self._config:
            if record['ip'] == ip:
                crypto = pwd_crypt()
                password = crypto.decrypt(record['password'])
                ret_record = copy(record)
                ret_record['password'] = password
        return ret_record

    def modify_record(self, ip, port = None, user = None, password = None):
        # 检查是否有对应的ip，如果没有则抛出错误
        if password != None:
            crypto = pwd_crypt()
            password = crypto.encrypt(password)
        a_record = 0
        for record in self._config:
            if record['ip'] == ip:
                # 找到了对应的记录
                a_record= 1
                for key in record:
                    # 如果记录中的这个参数在上下文中并且数据不是None, 则把与参数同名的上下文变量的值赋值给参数
                    if key in locals() and locals()[key] != None:
                        record[key] = locals()[key]
                self._sync()
                return
        
        if a_record == 0:
            raise self.ErrorNotFind
        
        
