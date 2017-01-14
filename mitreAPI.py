#!/usr/bin/env python

import argparse
import requests
import urllib
#OR
from requests.utils import quote
quote('/test', safe='')

# Argparse 
ap = argparse.ArgumentParser(description='Pull data from Mitre\'s ATT&CK site.')
ap.add_argument('--Technique', '-T', help='Technique')
ap.add_argument('--tactic', '-t', help='tactic')
ap.add_argument('--dump', '-d', action='store_true', help='Dump all data')
args = ap.parse_args()

## query
## configurable query page selectors? https://www.semantic-mediawiki.org/wiki/Help:Selecting_pages
## configurable printout statemetns? https://www.semantic-mediawiki.org/wiki/Help:Displaying_information 

# Variables for Mitre
# Replace this with functions to accept args 
if args.dump:
	query = '%5B%5BCategory%3ATechnique%5D%5D%7C%3FHas%20tactic%7C%3FHas%20ID%7C%3FHas%20display%20name%7Climit%3D9999'
host = 'https://attack.mitre.org'
url = '/api.php?action=ask&format=json&query=%s' %query
tactic = args.tactic
technique = args.Technique

# create list of arguments
arg_list = []

# Function to URL encode query data
def url_encode(arg):
	u = urllib.quote('%s' %arg, safe='')
	arg_list.append(u)

# this will be a function that populates query based on arguments from argparse
def mk_query(arg_list):
	q = url_encode(arg)
	
# Request data
r = requests.get('%s%s%s'%(host, url, query))

# Parse JSON response
#print r.json()
res = r.json()['query']['results']
print res['Technique/T1009']
#print res


# Function to retrieve all data
#def get_all():

# Function to output data

