#coding=utf-8
import sys

# 参数辅助类
class usage_helper:
    def __init__(self,application,action,parameter_descs):
        self._parameters = parameter_descs
        self._application = application
        self._action = action
        pass

    # 根据参数表输出帮助信息
    def output(self):
        # 输出帮助信息的第一行，一般都是类似Usage: app list [abcde]这样的信息
        opts_string=''
        for opt in self._parameters:
            opts_string+=opt['name']
        print("Usage:%s %s [%s]" % (self._application, self._action, opts_string))

        # 循环输出参数信息
        for opt in self._parameters:
            # 为了保证输出的对齐，先格式化前半部分，比如"\t-u user"这一段，然后根据前半部分的长度，计算需要的空格数
            if opt['needarg'] == True:
                begin_with="\t-%s %s" % (opt['name'], opt['argname'])
            else:
                begin_with="\t-%s" % (opt['name'])
            print("%s%s%s" % (begin_with, " " * (30 - len(begin_with)), opt['desc']))

    # 根据参数表组织参数解析函数getopt所需要的第二个参数
    def get_opt_string(self):
        optstring=''
        for opt in self._parameters:
            if opt['needarg'] == True:
                optstring+='%s:' % (opt['name'])
            else:
                optstring+=opt['name']
        
        return  optstring
