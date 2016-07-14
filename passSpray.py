#!/usr/bin/env python

##########################
# Password spraying script
# Matthew Lange
# 6-22-2016
##########################

# import stuff
import pip

#psuedocode...
#sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev

def install_dependancy(package):
    pip.main(['install', package])

# create a dictionary of dependancies in the format 'import_format':'pip_install_format' 
dependancies = {'argparse':'argparse', 'ldap':'python-ldap'}

for key, value in dependancies.items():
    try:
	print "importing ", key
        import key
    except ImportError:
        try:
            install_dependancy(value)
            print "importing ", key
            import key
        except ImportError, e:
            print e

'''            
# Accept arguments
ap = argparse.ArgumentParser(description='This is a password spraying tool')
ap.add_argument('dc', type=str, help='domain controller', default=None)
ap.add_argument('--password', '-p', type=str, help='password to spray', default='password')
ap.add_argument('--log', '-l', help='write results to LOG', default='passSpray.log')
args = ap.parse_args()
'''

# Logging?

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
'''
