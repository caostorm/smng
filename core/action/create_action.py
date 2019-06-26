#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.globalvar import global_const

# 这个指令用来创建指令模板，协助进行指令开发
class action_create_action(server_action):
    __parameters__ = [
        {"name":"n", "needarg":True, "desc":"创建的模块的名称", "argname":"name"},
        {"name":"h", "needarg":False, "desc":"显示这条帮助信息"}
    ]
    def __init__(self):
        self.__usage_helper__ = usage_helper(sys.argv[0], "create_action", self.__parameters__)

    def __usage__(self):
        self.__usage_helper__.output()

    def description(self):
        return "为软件增加一个action，会在core/action内生成一个模版代码，可以添加自定义的功能到模版代码内"

    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self.__usage_helper__.get_opt_string())
        except Exception as e:
            self.__usage__()
            exit()
        for opt,arg in opts:
            if opt == '-h':
                self.__usage__()
                exit()
            elif opt == '-n':
                self._name_ = arg

    def run(self):
        # 模板代码
        tpl_code='''#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper

class action_%s(server_action):
    # 参数列表示例，可以在这边增加参数描述
    __parameters__ = [
        {"name":"h", "needarg":False, "desc":"显示这条帮助信息"}
    ]

    def __init__(self):
        # 创建帮助信息
        self.__usage_helper__ = usage_helper(sys.argv[0], "%s", self.__parameters__)

    def __usage__(self):
        # 输出action的帮助信息
        self.__usage_helper__.output()

    # action的简要描述，当执行smng help时，这个会输出到屏幕
    def description(self):
        return "填入action的简单介绍,这个介绍会在help action中输出"

    # 通用的参数解析方法，如果需要增加参数处理过程请在这个方法内添加
    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self.__usage_helper__.get_opt_string())
        except Exception as e:
            self.__usage__()
            exit()
        for opt,arg in opts:
            if opt == '-h':
                self.__usage__()
                exit()

    # action实际执行的动作，请将action的行为添加到这个方法内
    def run(self):
        pass
        '''%(self._name_, self._name_)
        with open("%s/core/action/%s.py"%(global_const().get_value('BASEDIR'), self._name_), "w+") as f:
            f.write(tpl_code)