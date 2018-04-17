#!/usr/bin/env python
import argparse
import requests
import urllib
import csv
import time

# Argparse 
ap = argparse.ArgumentParser(description='Pull data from Mitre\'s ATT&CK site.')
ap.add_argument('--Tactic', '-T', help='Dump all in Tactic')
ap.add_argument('--technique', '-t', help='Get technique by name')
ap.add_argument('--id', '-i', help='Get technique by id')
ap.add_argument('--dump', '-d', action='store_true', help='Dump all data')
ap.add_argument('--list_all', '-l', action='store_true', help='List all Tactics and Techniques')
args = ap.parse_args()

# Variables for Mitre
host = 'https://attack.mitre.org/api.php?action=ask&format=json&query='
data_query = '%7C%3FHas%20tactic%7C%3FHas%20ID%7C%3FHas%20display%20name%7C%3FHas%20technical%20description%7Climit%3D9999'
list_query = '%5B%5BCategory%3ATechnique%5D%5D%7C%3FHas%20tactic%7C%3FHas%20ID%7C%3FHas%20display%20name%7Climit%3D9999'

if args.Tactic:
	Tactic = args.Tactic.replace(',', '||')
if args.technique:
	technique = args.technique.replace(',', '||')
if args.id:
	tech_id = args.id.replace(',', '||')
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

# output to csv
def mk_csv_lst():
	csv_out = list()
        headers = ['Tactic','Technique','ID','Technical Description']
	csv_out.append(headers)
	for i in res:
		p = res[i]['printouts']
		tactic = str(p['Has tactic'][0]['fulltext'])
                #tactic = list()
                #for t in p['Has tactic']:
                    #tactic.append(str(t['fulltext']))
		technique = str(p['Has display name'][0])
		tid = str(p['Has ID'][0])
                if not args.list_all:
		    description = str(p['Has technical description'][0])
		    data = [tactic, technique, tid, description]
                else:
                    print 'Tactic: %s\nID:%s\nTechnique: %s\n' %(tactic, tid, technique)
		    data = [tactic, technique, tid]
		csv_out.append(data)
	#print csv_out
	return csv_out

# Function to output data to csv
def mk_csv_file(csv_out):
	date = time.strftime("%Y-%m-%d")
	with open('mitre_data-%s.csv' %date, "wb") as out_file:
		wr = csv.writer(out_file, dialect='excel')
		wr.writerows(csv_out)

# Construct query
if args.dump:
	query = '%5B%5BCategory%3ATechnique%5D%5D' + data_query
elif args.Tactic:
	u_query = mk_query(Tactic, 'Tactic')
	query = url_encode(u_query) + data_query
elif args.technique:
	u_query = mk_query(technique, 'technique')
	query = url_encode(u_query) + data_query
elif args.id:
	u_query = mk_query(tech_id, 'tech_id')
	query = url_encode(u_query) + data_query
elif args.list_all:
        query = list_query
else:
	print 'Invalid arguments'
	exit(0)

# Request data and parse JSON response
r = requests.get('%s%s'%(host, query))
res = r.json()['query']['results']

c = mk_csv_lst()

if not args.list_all:
	mk_csv_file(c)
