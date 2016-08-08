#!/usr/bin/env python

###########################################################
# parse OpenIOC file for IOCs to create CS MC2 Profile
# OpenIOC parsing stolen from: http://www.jeffbryner.com/blog/itsec/pythoniocdump.html
# Matt Lange
# 7-29-2016
############################################################

import lxml.objectify as lo
from collections import defaultdict
import argparse
import logging

logging.basicConfig(format='[+}%(levelname)s:%(message)s', level=logging.DEBUG)

ap = argparse.ArgumentParser(description='Parse OpenIOC files. Create Cobalt Strike Malleable C2 Profile config files.')
ap.add_argument('iocFile', type=str, help='OpenIOC file to parse')
ap.add_argument('--write', '-w', help='Parse and write a CS MC2 Profile named [file].')
ap.add_argument('--sleeptime', '-s', help='set sleeptime in miliseconds, default is 30000', default=30000)
ap.add_argument('--jitter', '-j', help='set jitter in seconds, default value is zero', default=0)
args = ap.parse_args()

# Dictionary of IOCs that are useful in a CS MC2 Profile config mapped to CS MC2 keywords
# might be more in the 'UrlHistoryItem' and 'CookieHistoryItem' categories (http://openioc.org/terms/Current.iocterms)
iocs = {
'Network/URI':'uri',
'Network/UserAgent':'useragent',
'Network/HTTP_Referr':'Referer',
'Network/DNS':'Host',
#'PortItem/remoteIP':'?'
}

def parse_ioc(ioc_in):
	ioco = lo.parse(ioc_in)
	parse_root = ioco.getroot()
	return parse_root

def create_ioc_dict(root):
	# Create dictionary to store ioc key-value pairs. defaultdict(list) stores dup keys values as a list 
	temp_dict = defaultdict(list)
	
	# Store values of the IOC keys we care about for MC2 Profiles
	for i in root.xpath("//*[local-name()='IndicatorItem']"):
		if i.Context.attrib.get("search") in iocs:
			temp_dict[iocs[i.Context.attrib.get("search")]].append(i.Content)
	return temp_dict

def print_ioc(root):
	print("Description:\n%s: %s"%(root.short_description, root.description))
	
	# Print values of the IOC keys we care about for MC2 Profiles
	print "\nHere's the IOCs we probably care about for MC2 Profile creation\n"
	for i in root.xpath("//*[local-name()='IndicatorItem']"):
		if i.Context.attrib.get("search") in iocs:
			print('\t%s\t%s\t%s'%(i.getparent().attrib.get("operator"), i.Context.attrib.get("search"),i.Content))

	# Print all the remaining IOCs
	print "\nHere's all the rest of the IOCs in this file\n"
	for i in root.xpath("//*[local-name()='IndicatorItem']"):
		if i.Context.attrib.get("search") not in iocs:
			print('\t%s\t%s\t%s'%(i.getparent().attrib.get("operator"), i.Context.attrib.get("search"),i.Content))

class mk_profile():
	def __init__(self, ioc_dict, filename): 
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
		self.dictionary['preamble']['sleeptime'] = [args.sleeptime]
		self.dictionary['preamble']['jitter'] = [args.jitter]
		self.dictionary['preamble']['useragent'] = ioc_dict['useragent']
		self.dictionary['http-get']['uri'] = ioc_dict['uri']
		self.dictionary['http-post']['uri'] = ioc_dict['uri']
		self.dictionary['http-get']['client']['header']['Host'] = ioc_dict['Host']
		self.dictionary['http-post']['client']['header']['Host'] = ioc_dict['Host']
		self.dictionary['http-get']['client']['header']['Referer'] = ioc_dict['Referer']
		self.dictionary['http-post']['client']['header']['Referer'] = ioc_dict['Referer']

	def write_preamble(self, profile):
		for k, v in self.dictionary['preamble'].iteritems():
			if v:
				profile.write('set %s "%s";\n' %(k, v[0]))
			else:
				break

	def create_header_list(self, d, a_list):
		for k, v in d.iteritems():
			if isinstance(v, dict):
				a_list.append(k)
				create_header_list(v, a_list)
			elif isinstance(v, list):
				if v:
					a_list.append("\"{}\" \"{}\"".format(k, v[0]))
			else:
				a_list.append("\"{}\" \"{}\"".format(k, v))

	def write_http_get(self, profile):

		# Write the http-get container head and URI
		if self.dictionary['http-get']['uri']:
			profile.write('http-get {\n\tset uri "%s";\n' %self.dictionary['http-get']['uri'])
		else:
			profile.write('http-get {\n\tset uri "/index/";\n')

		# Write the client section
		profile.write('\tclient {\n') 

		# create and write the http-get client header list
		cl = list()
		self.create_header_list(self.dictionary['http-get']['client']['header'], cl)
		for i in cl:
			profile.write('\t\theader %s;\n' %i)

		# write standard Cobalt Strike http-get client metadata section and close 'client' section
		profile.write('\t\tmetadata {\n\t\t\tbase64;\n\t\t\theader "Cookie";\n\t\t}\n') 
		profile.write('\t}\n') 

		# Write the server section
		profile.write('\tserver {\n') 

		# create and write the http-get server 'header' list
		sl = list()
		self.create_header_list(self.dictionary['http-get']['server']['header'], sl)
		for i in sl:
			profile.write('\t\theader %s;\n' %i)

		# write standard Cobalt Strike http-get server output section and close the server and http-get sections
		profile.write('\t\toutput {\n\t\t\tbase64;\n\t\t\tprint;\n\t\t}\n') 
		profile.write('\t}\n}\n') 

	def write_http_post(self, profile):

		## Write the http-post container head and URI
		if self.dictionary['http-post']['uri']:
			profile.write('http-post {\n\tset uri "%s";\n' %self.dictionary['http-post']['uri'])
		else:
			profile.write('http-post {\n\tset uri "/index/";\n')

		## Write the http-post client section
		profile.write('\tclient {\n') 

		# create and write http-post client 'header' list
		cl = list()
		self.create_header_list(self.dictionary['http-post']['client']['header'], cl)
		for i in cl:
			profile.write('\t\theader %s;\n' %i)

		# write standard Cobalt Strike http-post client id and output sections
		profile.write('\t\tid {\n\t\t\tparameter "id";\n\t\t}\n')
		profile.write('\t\toutput {\n\t\t\tprint;\n\t\t}\n')

		# close out the client sections
		profile.write('\t\t}\n') 

		## Write the http-post server section
		profile.write('\tserver {\n') 

		# create and write the http-post server 'header' list
		sl = list()
		self.create_header_list(self.dictionary['http-post']['server']['header'], sl)
		for i in sl:
			profile.write('\t\theader %s;\n' %str(i))

		# write standard Cobalt Strike http-post server output section and close the server and http-post sections
		profile.write('\t\toutput {\n\t\t\tbase64;\n\t\t\tprint;\n\t\t}\n') 
		profile.write('\t\t}\n}\n') 

def main():
	logging.info('Parsing OpenIOC file: %s' %args.iocFile)
	ioc_root = parse_ioc(args.iocFile)
	logging.info('Extracting Cobalt Strike IOCs')
	cs_dict = create_ioc_dict(ioc_root)
	if args.write:
		m = mk_profile(cs_dict, args.write)
		with open(m.profile, 'a') as f:
			logging.info('Writing Cobalt Strike Profile file: %s' %m.profile)
			m.write_preamble(f)
			m.write_http_get(f)
			m.write_http_post(f)
	else:
		print_ioc(ioc_root)

if __name__ == "__main__" :
	main()
