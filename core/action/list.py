#coding=utf-8
import sys
import getopt
from core.interface.action import server_action
from core.helper.usage import usage_helper
from prettytable import PrettyTable
from core.helper.parser import config_parser
import re

class action_list(server_action):
    # 参数列表示例，可以在这边增加参数描述，最终代码将根据argname生成对对应的参数
    _parameters = [
        {"name":"h", "needarg":False, "desc":"显示这条帮助信息", "argname":"help"},
        {"name":"n", "needarg":True, "desc":"根据服务器名称进行模糊搜索", "argname":"name"},
        {"name":"t", "needarg":True, "desc":"根据标签进行搜索", "argname":"tag"}
    ]

    def __init__(self):
        # 创建帮助信息
        self._usage_helper = usage_helper(sys.argv[0], "list", self._parameters)
        self._config = config_parser()

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
        return "列出服务器信息"

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
        self._tag=[]
        prog_with_value = re.compile(r'^[\w]+=[0-9a-zA-Z-_]+$')
        prog_without_value = re.compile(r'^[\w]+$')
        for opt, arg in opts:
            if opt == '-t':
                if prog_with_value.match(arg) is not None:
                    # 带值的标签，例如tag=hello
                    name,value = arg.split('=')
                    self._tag.append({name:value})
                elif prog_without_value.match(arg) is not None:
                    # 不带值的标签，例如tag
                    self._tag.append({arg:''})
                else:
                    print("%s is bad value"%(arg))

    # 根据服务器名称进行模糊搜索，如果没有要求名称搜索，则返回全集
    def _search_by_name(self):
        ret_array = []
        # 不需要使用名称进行过滤时，返回全集
        if self._name == None:
            for i in self._config:
                ret_array.append(i['ip'])
            return set(ret_array)
        # 否则进行模糊搜索，把搜索出来的ip放到集合
        prog = re.compile('^.*%s.*$'%(self._name))
        for i in self._config:
            if 'name' not in i:
                continue
            if prog.match(i['name']) != None:
                ret_array.append(i['ip'])
        return set(ret_array)

    # 根据服务器的标签进行搜索，如果没有要求标签进行搜索，则返回全集
    def _search_by_tag(self):
        ret_array = []
        # 没有使用tag筛选，返回全集
        if len(self._tag) == 0:
            for i in self._config:
                ret_array.append(i['ip'])
            return set(ret_array)
        # 格式化tag输入参数
        for i in self._config:
            if 'tags' in i:
                print(i['tags'])
        return set([])
        pass

    # action实际执行的动作，请将action的行为添加到这个方法内
    def run(self):
        # 先按照参数过滤
        name_set = self._search_by_name()
        tag_set = self._search_by_tag()
        finnal_set = name_set & tag_set
        prog = re.compile('^%s$'%(self._name))
        disp = PrettyTable(["IP", "服务器名称","标签"])
        for i in self._config:
            # 检测记录是否在搜索结果内
            if i['ip'] in finnal_set:
                name = i['name'] if 'name' in i else ''
                tag = []
                if 'tags' in i:
                    for t in i['tags']:
                        tag.append("%s:%s"%(t, i['tags'][t]))
                disp.add_row([i['ip'], name, ','.join(tag)])
        print(disp)
        