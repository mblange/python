#!/usr/bin/env python

###########################################################
# parse OpenIOC file for IOCs to create CS MC2 Profile
# basically just stolen (and modified) from:
# http://www.jeffbryner.com/blog/itsec/pythoniocdump.html
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

# Print IOCs we care about for Malleable C2 Profiles
print "\nHere's the IOCs we probably care about for Malleable C2 Profile creation\n"
for ii in root.xpath("//*[local-name()='IndicatorItem']"):
	if ii.Context.attrib.get("search") in iocs:
		print('\t%s\t%s\t%s'%(ii.getparent().attrib.get("operator"), ii.Context.attrib.get("search"),ii.Content))
		ioc_map[ii.Context.attrib.get("search")] = ii.Content
		print ioc_map[ii.Context.attrib.get("search")]

# Print all the IOCs
print "\nHere's all the rest of the IOCs in this file\n"
for ii in root.xpath("//*[local-name()='IndicatorItem']"):
	if ii.Context.attrib.get("search") not in iocs:
		print('\t%s\t%s\t%s'%(ii.getparent().attrib.get("operator"), ii.Context.attrib.get("search"),ii.Content))
