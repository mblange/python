#!/usr/bin/env python

##########################
# Password spraying script
# Matthew Lange
# 6-22-2016
##########################
import sys
## import stuff
dependancies = ['logging', 'argparse', 'ldap', 'subprocess', 'os']

for d in dependancies:
    try:
		print "importing %s" %d
		d = __import__(d)
    except ImportError, e:
		print "failed to import %s. Try 'pip install %s'" %(d, d)
		print >> sys.stderr, "Exception: %s" % str(e)
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
def logger(oFunc):
	logging.basicConfig(filename='%s' %(args.log), level=logging.INFO)
	def wrapper(*args, **kwargs):
		logging.info('%s: Started' %(oFunc.__name__))
		oFunc(*args, **kwargs)
		logging.info('%s: Finished'%(oFunc.__name__))
	return wrapper

@logger
def do_something(msg):
	print msg

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
