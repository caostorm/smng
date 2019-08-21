#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper
from core.helper.config import options_config

class action_config(server_action):
    # 参数列表示例，可以在这边增加参数描述，最终代码将根据argname生成对对应的参数
    _parameters = [
        {"name":"h", "needarg":False, "desc":"显示这条帮助信息", "argname":"help"}
    ]

    def __init__(self):
        # 创建帮助信息
        self._usage_helper = usage_helper(sys.argv[0], "config", self._parameters)

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
            parameter_name = "_%s"%(obj['argname'])
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
                setattr(self,"_%s"%(parameters[opt]['argname']), arg)      # 需要传入值的参数设置值
            else:
                setattr(self,"_%s"%(parameters[opt]['argname']), True)     # 不需要传入值的参数设置成True
        # 单独处理help参数，默认输出帮助信息
        if self._help == True:
            self._usage()
            exit()
        # ToDo: 自定义的解析方法
        self._config = []
        for parameter in argv:
            self._config.append(parameter.split('='))
        pass

    # action实际执行的动作，请将action的行为添加到这个方法内
    def run(self):
        cfg = options_config()
        for k,v in self._config:
            cfg.write(k,v)
        pass
        