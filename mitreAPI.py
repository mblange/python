#!/usr/bin/env python

import argparse
import requests
import urllib
#OR
from requests.utils import quote
quote('/test', safe='')

# Argparse 
ap = argparse.ArgumentParser(description='Pull data from Mitre\'s ATT&CK site.')
ap.add_argument('--Tactic', '-t', help='Tactic')
ap.add_argument('--technique', '-T', help='technique')
ap.add_argument('--display', '-d', help='tactic')
ap.add_argument('--Dump', '-D', action='store_true', help='Dump all data')
args = ap.parse_args()

## query
## configurable query page selectors? https://www.semantic-mediawiki.org/wiki/Help:Selecting_pages
## configurable printout statemetns? https://www.semantic-mediawiki.org/wiki/Help:Displaying_information 

# Variables for Mitre
# Replace this with functions to accept args 
if args.Dump:
	query = '%5B%5BCategory%3ATechnique%5D%5D%7C%3FHas%20tactic%7C%3FHas%20ID%7C%3FHas%20display%20name%7C%3FHas%20technical%20description%7Climit%3D9999'
host = 'https://attack.mitre.org'
url = '/api.php?action=ask&format=json&query=%s' %query
tactic = args.Tactic
technique = args.technique
display_parameter = args.display

# create list of arguments
arg_list = []

# Function to URL encode query data
def url_encode(arg):
	u = urllib.quote('%s' %arg, safe='')
	arg_list.append(u)

# this will be a function that populates query based on arguments from argparse
def mk_query(arg_list):
	for arg in arg_list:
		continue

# Request data
r = requests.get('%s%s%s'%(host, url, query))

# Parse JSON response
res = r.json()['query']['results']
#print res
for i in res:
	p = res[i]['printouts']
	print 'Tactic: %s\n%s: %s\n%s\n' %(p['Has tactic'][0]['fulltext'], i, p['Has display name'][0], p['Has technical description'][0])


# Function to retrieve all data
#def get_all():

# Function to output data

