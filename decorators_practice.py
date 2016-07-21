#!/usr/bin/env python

######################
# practice decorators
######################

def decorator_func(orig_func):
	def wrapper_func():
		return orig_func()

	return wrapper_func

def display():
	print('display function ran')

decorated_display = decorator_func(display)

decorated_display()
