#!/usr/bin/env python
from sys import argv
import re
import random

tor = [t.rstrip('\n') for t in open("tor.txt")]
randomIP = [r.rstrip('\n') for r in open("random.txt")]

with open(argv[1], "r") as fin:
	for line in fin:
		content = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
		if content[1] == '172.21.22.226':
			#swap with tor	
			re.sub('172\.21\.22\.226', random.choice(tor), line)
			print 'tor'
		elif content[1] == '172.21.22.181':
			#swap with randomIP
			re.sub('172\.21\.22\.181', random.choice(randomIP), line)
			print 'random'
		else:
			print "nope"
			continue
