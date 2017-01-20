#!/usr/bin/env python
## configurable query page selectors? https://www.semantic-mediawiki.org/wiki/Help:Selecting_pages
## configurable printout statemetns? https://www.semantic-mediawiki.org/wiki/Help:Displaying_information 
import argparse
import requests
import urllib
import csv
import time

# Argparse 
ap = argparse.ArgumentParser(description='Pull data from Mitre\'s ATT&CK site.')
ap.add_argument('--Tactic', '-T', help='Dump all in Tactic')
ap.add_argument('--technique', '-t', help='Get technique by name')
ap.add_argument('--tid', '-i', help='Get technique by id')
ap.add_argument('--dump', '-d', action='store_true', help='Dump all data')
ap.add_argument('--list_all', '-l', action='store_true', help='List all Tactics and Techniques')
args = ap.parse_args()

#TODO: Dump all [x], Dump all techniques in Tactic [ ], Get technique by: Name [ ], ID [ ], List Tactics [ ], List techniques [ ].

# Variables for Mitre
host = 'https://attack.mitre.org/api.php?action=ask&format=json&query='
data_query = '%7C%3FHas%20tactic%7C%3FHas%20ID%7C%3FHas%20alias%7C%3FHas%20display%20name%7C%3FHas%20platform%7C%3FHas%20technical%20description%7Climit%3D9999'
list_query = '%5B%5BCategory%3ATechnique%5D%5D%7C%3FHas%20tactic%7C%3FHas%20ID%7C%3FHas%20display%20name%7Climit%3D9999'

if args.Tactic:
	Tactic = args.Tactic.replace(',', '||')
if args.technique:
	technique = args.technique.replace(',', '||')
if args.tid:
	tech_id = args.tid.replace(',', '||')
if args.list_all:
	query = list_query

# Populate query based on arguments from argparse
def mk_query(arg, arg_type):
	if arg_type == 'Tactic':
		Tactic = "[[Has tactic::%s]]" %(arg)
		return Tactic
	if arg_type == 'technique':
		technique = "[[Has display name::%s]]" %(arg)
		return technique
	if arg_type == 'tech_id':
		tech_id = "[[Has ID::%s]]" %(arg)
		return tech_id

# Function to URL encode query data
def url_encode(arg):
	return urllib.quote('%s' %arg, safe='')

# Construct query
if args.dump:
	query = '%5B%5BCategory%3ATechnique%5D%5D' + data_query
elif args.Tactic:
	u_query = mk_query(Tactic, 'Tactic')
	query = url_encode(u_query)
elif args.technique:
	u_query = mk_query(technique, 'technique')
	query = url_encode(u_query)
elif args.tid:
	u_query = mk_query(tech_id, 'tech_id')
	query = url_encode(u_query)
else:
	exit(0)
query = query + data_query

# Request data
r = requests.get('%s%s'%(host, query))

# Parse JSON response
res = r.json()['query']['results']
#print res
if not args.list_all:
	for i in res:
		p = res[i]['printouts']
		print 'Tactic: %s\n%s: %s\nAlias: %s\n%s\n' %(p['Has tactic'][0]['fulltext'], i, p['Has display name'][0], p['Has alias'], p['Has technical description'][0])
else:
	print query

# Function to output data (to csv?)
