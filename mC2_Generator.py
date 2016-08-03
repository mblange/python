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
ap.add_argument('iocFile', type=str, help='OpenIOC file')
ap.add_argument('--write', '-w', help='Parse and write a CS MC2 Profile.')
ap.add_argument('--sleeptime', '-s', help='set sleeptime value for CS', default=30000)
args = ap.parse_args()

# Dictionary of IOCs that are useful in a CS MC2 Profile config mapped to CS MC2 keywords
iocs = {
'Network/URI':'uri',
'Network/UserAgent':'useragent',
'Network/HTTP_Referr':'Referer',
'Network/DNS':'??',
'PortItem/remoteIP':'Host:'
}

def parse_ioc(ioc_in):
	ioco = lo.parse(ioc_in)
	parse_root = ioco.getroot()
	return parse_root

def print_ioc(root):
	# Create dictionary to store ioc key-value pairs. defaultdict(list) stores dup keys values as a list 
	temp_dict = defaultdict(list)
	print("Description:\n%s: %s"%(root.short_description, root.description))
	
	# Print & store values of the IOC keys we care about for MC2 Profiles
	print "\nHere's the IOCs we probably care about for MC2 Profile creation\n"
	for i in root.xpath("//*[local-name()='IndicatorItem']"):
		if i.Context.attrib.get("search") in iocs:
			print('\t%s\t%s\t%s'%(i.getparent().attrib.get("operator"), i.Context.attrib.get("search"),i.Content))
			# and add them to our dictionary
			temp_dict[iocs[i.Context.attrib.get("search")]].append(i.Content)

	# Print all the remaining IOCs
	print "\nHere's all the rest of the IOCs in this file\n"
	for i in root.xpath("//*[local-name()='IndicatorItem']"):
		if i.Context.attrib.get("search") not in iocs:
			print('\t%s\t%s\t%s'%(i.getparent().attrib.get("operator"), i.Context.attrib.get("search"),i.Content))

	return temp_dict

class mk_profile():
	def __init__(self, ioc_dict, filename): 
		## create file here?
		self.profile = '{}.profile'.format(filename)
		# create dictionary
		self.dictionary = dict()
		self.dictionary['preamble'] = dict() 
		self.dictionary['http-get'] = dict() 
		self.dictionary['http-get']['uri'] = dict()
		self.dictionary['http-get']['client'] = dict()
		self.dictionary['http-get']['server'] = dict()
		self.dictionary['http-get']['client']['header'] = dict()
		self.dictionary['http-get']['server']['header'] = dict()
		self.dictionary['http-get']['client']['metadata'] = dict()
		self.dictionary['http-get']['server']['output'] = dict()
		self.dictionary['http-post'] = dict() 
		self.dictionary['http-post']['uri'] = dict()
		self.dictionary['http-post']['client'] = dict()
		self.dictionary['http-post']['server'] = dict()
		self.dictionary['http-post']['client']['header'] = dict()
		self.dictionary['http-post']['server']['header'] = dict()
		self.dictionary['http-post']['client']['output'] = dict()
		self.dictionary['http-post']['server']['output'] = dict()
		self.dictionary['http-post']['client']['id'] = dict()
		# insert values into dictionary
		self.dictionary['http-get']['client']['header']['Referer'] = ioc_dict['Referer']
		self.dictionary['http-post']['client']['header']['Referer'] = ioc_dict['Referer']
		self.dictionary['http-get']['client']['header']['Host'] = ioc_dict['Host']
		self.dictionary['http-post']['client']['header']['Host'] = ioc_dict['Host']
		self.dictionary['http-get']['uri'] = ioc_dict['uri']
		self.dictionary['http-post']['uri'] = ioc_dict['uri']
		self.dictionary['preamble']['useragent'] = ioc_dict['useragent']
		self.dictionary['preamble']['sleeptime'] = ioc_dict['args.sleeptime']

	def write_preamble(self, profile):
		for k, v in self.dictionary['preamble'].iteritems():
			if v:
				profile.write('set %s "%s";\n' %(k, v))
			else:
				break
	def write_header(self, d, a_list):
		for k, v in d.iteritems():
			if isinstance(v, dict):
				a_list.append(k)
				write_header(v, a_list)
			else:
				a_list.append({k:v})

	def write_http_get(self, profile):
		cl = list()
		sl = list()

		# Write the http-get container head and URI
		profile.write('http-get {\n\tset uri "%s";\n' %self.dictionary['http-get']['uri'])

		# Write the client section
		self.write_header(self.dictionary['http-get']['client']['header'], cl)
		profile.write('\tclient {\n') 
		for i in cl:
			profile.write('\t\theader %s;\n' %i)
		profile.write('\t\tmetadata {\n\t\t\tbase64;\n\t\t\theader "Cookie";\n\t\t}\n') 
		profile.write('\t}\n') 

		# Write the server section
		self.write_header(self.dictionary['http-get']['server']['header'], sl)
		profile.write('\tserver {\n') 
		for i in sl:
			profile.write('\t\theader %s;\n' %str(i))
		profile.write('\t\toutput {\n\t\t\tbase64;\n\t\t\tprint;\n\t\t}\n') 
		profile.write('\t}\n}\n') 

	def write_http_post(self, profile):
		cl = list()
		sl = list()

		# Write the http-post container head and URI
		profile.write('http-post {\n\tset uri "%s";\n' %self.dictionary['http-get']['uri'])

		# Write the client section
		self.write_header(self.dictionary['http-post']['client']['header'], cl)
		profile.write('\tclient {\n') 
		for i in cl:
			profile.write('\t\theader %s;\n' %i)
		profile.write('\t\tid {\n\t\t\tparameter "id";\n\t\t}\n')
		profile.write('\t\toutput {\n\t\t\tprint;\n\t\t}\n')
		profile.write('\t\t}\n') 

		# Write the server section
		self.write_header(self.dictionary['http-post']['server']['header'], sl)
		profile.write('\tserver {\n') 
		for i in sl:
			profile.write('\t\theader %s;\n' %str(i))
		profile.write('\t\toutput {\n\t\t\tbase64;\n\t\t\tprint;\n\t\t}\n') 
		profile.write('\t\t}\n}\n') 
'''
	def http_post(self):
		print "http_post"

'''

def main():
	global m # for testing only. delete this later 
	global cs_dict
	root = parse_ioc(args.iocFile)
	cs_dict = print_ioc(root)
	if args.write:
		m = mk_profile(cs_dict, args.write)
		print m.dictionary
		with open(m.profile, 'a') as f:
			m.write_preamble(f)
			m.write_http_get(f)
			m.write_http_post(f)
	else:
		pass

if __name__ == "__main__" :
	main()
