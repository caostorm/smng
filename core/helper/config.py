#coding=utf-8
import json
from core.helper.crypt import pwd_crypt
from core.helper.globalvar import global_const
import sys

class options_config:
    class ErrorTypeNotSupport(BaseException):
        def __init__(self):
            pass

        def __str__(self):
            return "This type didn't support"

    def __init__(self):
        self._config_file_path = global_const().get_value('BASEDIR') + "/etc/options.json"
        with open(self._config_file_path, "a+") as f:
            try:
                # 读取文件，从文件初始化_config对象
                f.seek(0)
                self._config = json.loads(f.read())
            except:
                self._config = {}

    def _sync_file(self):
        with open(self._config_file_path, "w+") as f:
            f.write(json.dumps(self._config))
        pass

    def write(self, key, value):
        obj = {}
        if type(value) == type('1.2'):
            # string
            obj['type'] = 'string'
        elif type(value) == type(1.2):
            # float
            obj['type'] = 'float'
        elif type(value) == type(1):
            # int
            obj['type'] = 'int'
        elif type(value) == type(True):
            # bool
            obj['type'] = 'bool'
        else:
            if sys.version_info.major == 2:
                if type(value) == type(1L):
                    obj['type'] = long
                else:
                    raise self.ErrorTypeNotSupport
            else:
                raise self.ErrorTypeNotSupport
        encrypto = pwd_crypt()
        obj['value'] = encrypto.encrypt(str(value))
        self._config[key] = obj
        self._sync_file()

    def read(self, key):
        obj = self._config[key]
        encrypto = pwd_crypt()
        if obj['type'] == 'string':
            return str(encrypto.decrypt(obj['value']))
        elif obj['type'] == 'float':
            return float(encrypto.decrypt(obj['value']))
        elif obj['type'] == 'int':
            return int(encrypto.decrypt(obj['value']))
        elif obj['type'] == 'bool':
            real_value = encrypto.decrypt(obj['value'])
            if 'True' == real_value:
                return True
            elif 'False' == real_value:
                return False
        elif obj['type'] == 'long':
            return long(encrypto.decrypt(obj['value']))


