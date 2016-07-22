#!/usr/bin/env python

##########################
# Password spraying script
# Matthew Lange
# 6-22-2016
##########################

## import stuff
try:
	import sys
	import logging
	import argparse
	import ldap
	import time

except ImportError, e:
	print "Exception: %s. Try 'pip install [module_name]'" % str(e)
	sys.exit(1)

##psuedocode...
#sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev

# Accept arguments
ap = argparse.ArgumentParser(description='This is a password spraying tool')
ap.add_argument('dc', type=str, help='domain controller', default=None)
ap.add_argument('--password', '-p', type=str, help='password to spray', default='password')
ap.add_argument('--log', '-l', help='write results to LOG', default='passSpray.log')
args = ap.parse_args()

# Logging?
def logger(orig_func):
	logging.basicConfig(filename='%s' %(args.log), level=logging.INFO)
	def wrapper(*args, **kwargs):
		logging.info('%s: Started at:\t%s' %(orig_func.__name__, time.asctime(time.localtime(time.time()))))
		orig_func(*args, **kwargs)
		logging.info('%s: Finished at:\t%s' %(orig_func.__name__, time.asctime(time.localtime(time.time()))))
	return wrapper

@logger
def do_something(msg):
	print msg

do_something('hi')

# Establish some variables
    # discover DC's
    # set username and password to use to connect to DC and pull user list
    # set password to spray

# Get domain username list
    # connect to DC
    # request list of domain usernames
    # write to tmp file for later use


# Spray passwords against DC
    # reconnect to DC by looping through users with a password
        # log results
