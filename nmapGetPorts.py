#!/usr/bin/env python

###############################################################
# Parse nmap xml output and print comma separated list of ports
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

# Accept argument containing an Nmap xml 'file' to parse
ap = argparse.ArgumentParser(description='parser to retrieve ports from nmap scan')
ap.add_argument('file', type=str, help='nmap.xml output file to parse', default=None)
args = ap.parse_args()

# Parse the file and create 'obj' handler
obj = untangle.parse('%s' %(args.file))

# Establish handler for all port data
port_data = obj.nmaprun.host.ports.port

# Establish empty list for storing ports
ports = []

# Iterate through all ports and append them to the 'ports' list
for p in range(len(port_data)):
        ports.append(int(port_data[p]['portid']))

# Print comma-separated list
print ','.join(str(i) for i in ports)
