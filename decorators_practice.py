#!/usr/bin/env python

######################
# practice decorators
######################
from functools import wraps

def my_logger(orig_func):
	import logging
	logging.basicConfig(filename='{}.log'.format(orig_func.__name__), filemode='w', level=logging.DEBUG)

	@wraps(orig_func)
	def wrapper_func(*args, **kwargs):
		logging.info('%s Started with args: %s and kwargs:  %s' %(orig_func.__name__, args, kwargs))
		return orig_func(*args, **kwargs)
		# logging.info('%s stopped' %(orig_func.__name__, ))

	return wrapper_func

def my_timer(orig_func):
	import time

	@wraps(orig_func)
	def wrapper_func(*args, **kwargs):
		t1 = time.time()
		result = orig_func(*args, **kwargs)
		t2 = time.time() - t1
		print('%s ran in %s seconds' %(orig_func.__name__, t2))
		return result

	return wrapper_func

#@my_logger
#def display():
#	print('display function ran')

@my_timer
@my_logger
def display_info(name, age):
	print 'display info: %s is %d' %(name, age)

display_info('jon', 25)
