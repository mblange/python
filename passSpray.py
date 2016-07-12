#!/usr/bin/env python

##########################
# Password spraying script
# Matthew Lange
# 6-22-2016
##########################

# import stuff
import pip

def install_dependancy(package):
    pip.main(['install', package])

dependancies = {'argparse':'argparse', 'ldap':'python-ldap'}

for key, value in dependancies.items():
    try:
        import key
    except ImportError, e:
        install_dependancy(value)
'''
# Accept arguments
ap = argparse.ArgumentParser(description='This is a password spraying tool')
ap.add_argument('dc', type=str, help='domain controller', default=None)
ap.add_argument('--password', '-p', type=str, help='password to spray', default='password')
ap.add_argument('--log', '-l', help='write results to LOG', default='passSpray.log')
args = ap.parse_args()

# Logging?

# Get domain username list
    # connect to DC
    # request users
    # write to tmp file for later use


# Spray passwords against DC
    # connect to DC
    # loop through users with a password
    # log results
'''
