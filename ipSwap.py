#!/usr/bin/env python
import argv
import re
import random

tor = []
randomIP = []

with open(argv[1], "r") as fin
	for line in fin:
		content = re.findall(r'172\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
		if content[1] == '172.21.22.226':
			#swap with tor	
			re.sub('172\.21\.22\.226', random.choice(tor), line)
		else:
			#swap with randomIP
			re.sub('172\.21\.22\.xxx', random.choice(randomIP), line)
