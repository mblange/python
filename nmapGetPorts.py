#!/usr/bin/env python

###############################################################
# parse nmap xml output and print comma separated list of ports
# matt lange
# 7/25/16
###############################################################
## import stuff

import sys

try:
	import untangle
	import argparse

except ImportError, e:
	print "Exception: %s. Try 'pip install [module_name]'" % str(e)
	sys.exit(1)

ap = argparse.ArgumentParser(description='parser to retrieve ports from nmap scan')
ap.add_argument('file', type=str, help='nmap.xml output file to parse', default=None)
args = ap.parse_args()

obj = untangle.parse('%s' %(args.file))

ports = []

for p in range(len(obj.nmaprun.host.ports.port)-1):
	ports.append(int(obj.nmaprun.host.ports.port[p]['portid']))

print ','.join(str(i) for i in ports)
