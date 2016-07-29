#!/usr/bin/env python

###########################################################
# parse OpenIOC file for IOCs to create CS MC2 Profile
# Based on: http://www.jeffbryner.com/blog/itsec/pythoniocdump.html
# Matt Lange
# 7-29-2016
############################################################

import sys
import lxml.objectify

iocs = [
'Network/URI',
'Network/UserAgent',
'Network/HTTP_Referr',
'Network/DNS',
'PortItem/remoteIP'
]

# Dictionary to map openIOC search value to CS MC2
ioc_map = {'Network/URI':'', 'Network/UserAgent':'', 'Network/HTTP_Referr':'', 'Network/DNS':'', 'PortItem/remoteIP':''}

ioco = lxml.objectify.parse(sys.argv[1])
root = ioco.getroot()

print("Description:\n%s: %s"%(root.short_description, root.description))

# Print & store values of the IOC keys we care about for MC2 Profiles
print "\nHere's the IOCs we probably care about for MC2 Profile creation\n"
for ii in root.xpath("//*[local-name()='IndicatorItem']"):
	if ii.Context.attrib.get("search") in iocs:
		print('\t%s\t%s\t%s'%(ii.getparent().attrib.get("operator"), ii.Context.attrib.get("search"),ii.Content))
		ioc_map[ii.Context.attrib.get("search")] = ii.Content

# Print all the IOCs
print "\nHere's all the rest of the IOCs in this file\n"
for ii in root.xpath("//*[local-name()='IndicatorItem']"):
	if ii.Context.attrib.get("search") not in iocs:
		print('\t%s\t%s\t%s'%(ii.getparent().attrib.get("operator"), ii.Context.attrib.get("search"),ii.Content))

print ioc_map

# TODO: write to CS MC2 Profile
with open('new.profile', 'w') as file:
	file.write(str(ioc_map))
	
