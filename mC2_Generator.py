#!/usr/bin/env python

###########################################################
# parse OpenIOC file for IOCs to create CS MC2 Profile
# Based on: http://www.jeffbryner.com/blog/itsec/pythoniocdump.html
# Matt Lange
# 7-29-2016
############################################################

import lxml.objectify as lo
from collections import defaultdict
import argparse

# Accept arguments. Include option to only parse and print the ioc file not create mc profile 
ap = argparse.ArgumentParser(description='Parse OpenIOC files. Create CS MC2 Profile config files.')
#group = ap.add_mutually_exclusive_group()
ap.add_argument('iocFile', type=str, help='OpenIOC file')
ap.add_argument('--write', '-w', help='Parse and write a CS MC2 Profile.')
args = ap.parse_args()

# List of IOCs that are useful in a CS MC2 Profile config
iocs = [
'Network/URI',
'Network/UserAgent',
'Network/HTTP_Referr',
'Network/DNS',
'PortItem/remoteIP'
]

def parse_ioc(ioc_in):
	ioco = lo.parse(ioc_in)
	parse_root = ioco.getroot()
	return parse_root

def print_ioc(root):
	# Create dictionary for storing ioc key-value pairs
	# defaultdict(list) makes duplicate keys store values in a list 
	print_ioc_dict = defaultdict(list)
	print("Description:\n%s: %s"%(root.short_description, root.description))
	
	# Print & store values of the IOC keys we care about for MC2 Profiles
	print "\nHere's the IOCs we probably care about for MC2 Profile creation\n"
	for i in root.xpath("//*[local-name()='IndicatorItem']"):
		if i.Context.attrib.get("search") in iocs:
			print('\t%s\t%s\t%s'%(i.getparent().attrib.get("operator"), i.Context.attrib.get("search"),i.Content))
			print_ioc_dict[i.Context.attrib.get("search")].append(i.Content)
	
	# Print all the IOCs
	print "\nHere's all the rest of the IOCs in this file\n"
	for i in root.xpath("//*[local-name()='IndicatorItem']"):
		if i.Context.attrib.get("search") not in iocs:
			print('\t%s\t%s\t%s'%(i.getparent().attrib.get("operator"), i.Context.attrib.get("search"),i.Content))
	return print_ioc_dict

class mk_profile():
	def __init__(self, ioc_dict, filename): 
		self.url = ioc_dict['Network/URI']
		self.useragent = ioc_dict['Network/UserAgent']
		self.referer = ioc_dict['Network/HTTP_Referr']
		self.domain =  ioc_dict['Network/DNS']
		self.ipaddress = ioc_dict['PortItem/remoteIP']
		self.profile = '{}.profile'.format(filename)
		
	def http_get(self):
		print "http_get"

	def http_post(self):
		print "http_post"

	def client(self):
		print "client"

	def server(self):
		print "server"

	## TODO: write to CS MC2 Profile
	#with open('new.profile', 'w') as file:
	#	file.write(str(ioc_dict))

def main():
	global m # for testing only. delete this later 
	root = parse_ioc(args.iocFile)
	ioc_dict = print_ioc(root)
	if args.write:
		m = mk_profile(ioc_dict, args.write)
		print m.useragent
		m.http_post()
	else:
		pass

if __name__ == "__main__" :
	main()
