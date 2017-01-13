#!/usr/bin/env python

import argparse
import requests

# Argparse goes here
## query
## configurable query page selectors? https://www.semantic-mediawiki.org/wiki/Help:Selecting_pages
## configurable printout statemetns? https://www.semantic-mediawiki.org/wiki/Help:Displaying_information 

# Variables for Mitre
host = 'https://attack.mitre.org'
# Replace this with functions to accept args 
query = '%5B%5BCategory%3ATechnique%5D%5D%7C%3FHas%20tactic%7C%3FHas%20ID%7C%3FHas%20display%20name%7Climit%3D9999'
url = '/api.php?action=ask&format=json&query=%s' %query
tactic = None #args.tactic
technique = None #args.technique

# this will be a function that populates query based on arguments from argparse

# Request data
r = requests.get('%s%s%s'%(host, url, query))
#print r.json()
res = r.json()['query']['results']
print res['Technique/T1009']

# Function to URL encode query data

# Function to retrieve all data
#def get_all():

# Function to parse JSON response

# Function to output data

