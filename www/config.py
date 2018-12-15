#！usr/bin/env python3
# -*- coding:utf-8 -*-

__author__='jingbin Zhao'

'''
Configuration.
'''
#为了简化读取配置文件，可以把所有配置读取到统一的config.py中
import config_default

class Dict(dict):
	'''
    Simple dict but support access as x.y style.
    '''
	"""
    重写属性设置，获取方法
    支持通过属性名访问键值对的值，属性名将被当做键名
    """
	def __init__(self,names=(),values=(),**kw):
		super(Dict,self).__init__(**kw)
		# zip函数将参数数据分组返回[(arg1[0],arg2[0],arg3[0]...),(arg1[1],arg2[1],arg3[1]...),,,]
        # 以参数中元素数量最少的集合长度为返回列表长度
		for k,v in zip(names,values):
			self[k]=v
	
	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
		
	def __setattr__(self,key,value):
		self[key]=value
		
def merge(defaults,override):
	r={}
	for k,v in defaults.items():
		if k in override:
			if isinstance(v,dict):
				r[k]=merge(v,override[k])
			else:
				r[k]=override[k]
		else:
			r[k]=v
	return r
	
def toDict(d):
	"""
        将一个dict转为Dict
    """
	D=dict()
	for k,v in d.items():
		D[k]=toDict(v) if isinstance(v,dict) else v
		#使用三目运算符，如果值是一个dict递归将其转换为Dict再赋值，否则直接赋值
	return D
	

configs=config_default.configs

try:
	import config_override
	configs=merge(configs,config_override.configs)
except ImportError:
	pass
	
configs=toDict(configs)

# Configuration,把default的host 替换成override的host，

# toDict(d):最后返回的是：

# {'db': {'host': '192.168.0.100'}}