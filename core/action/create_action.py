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
    # 参数列表示例，可以在这边增加参数描述，最终代码将根据argname生成对对应的参数
    _parameters = [
        {"name":"h", "needarg":False, "desc":"显示这条帮助信息", "argname":"help"}
    ]

    def __init__(self):
        # 创建帮助信息
        self._usage_helper = usage_helper(sys.argv[0], "%s", self._parameters)

    def _usage(self):
        # 输出action的帮助信息
        self._usage_helper.output()

    # 对参数进行预处理
    # 将参数描述数组重组成便于描述的字典，用于后续参数解析
    # 另外根据argname初始化参数，需要参数值的初始化成None，不需要参数值的初始化成False
    def _prepare_parameters(self):
        recognized_parameter={}
        for obj in self._parameters:
            obj_key = '-' + obj['name']     # 类似参数-h -n -a的样式作为字典的key
            recognized_parameter[obj_key] = obj    # 原参数描述的内容原封不动的存到字典里
            parameter_name = "_%%s"%%(obj['argname'])
            if obj['needarg'] == True:
                setattr(self, parameter_name, None)
            else:
                setattr(self, parameter_name, False)
        return recognized_parameter


    # action的简要描述，当执行smng help时，这个会输出到屏幕
    def description(self):
        return "填入action的简单介绍,这个介绍会在help action中输出"

    # 通用的参数解析方法，如果需要增加参数处理过程请在这个方法内添加
    def parse_parameters(self):
        try:
            opts, argv = getopt.getopt(sys.argv[2:], self._usage_helper.get_opt_string())
        except Exception as e:
            self._usage()
            exit()
        parameters = self._prepare_parameters()
        for opt,arg in opts:
            if parameters[opt]['needarg'] == True:
                setattr(self,"_%%s"%%(parameters[opt]['argname']), arg)      # 需要传入值的参数设置值
            else:
                setattr(self,"_%%s"%%(parameters[opt]['argname']), True)     # 不需要传入值的参数设置成True
        # 单独处理help参数，默认输出帮助信息
        if self._help == True:
            self._usage()
            exit()

    # action实际执行的动作，请将action的行为添加到这个方法内
    def run(self):
        pass
        '''%(self._name_, self._name_)
        with open("%s/core/action/%s.py"%(global_const().get_value('BASEDIR'), self._name_), "w+") as f:
            f.write(tpl_code)