#!/usr/bin/env python
from sys import argv
import re
import random

tor = [t.rstrip('\n') for t in open("tor.txt")]
randomIP = [r.rstrip('\n') for r in open("random.txt")]

with open(argv[1], 'rb') as fin:
	with open(argv[2], 'wb') as fout:
		for line in fin:
			line = line.strip()
			matches = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
			if matches:
				match = matches[1]
				if match == '172.21.22.226':
					#swap with tor	
					line = line.replace(match, random.choice(tor))
					fout.write(line + "\n")
				elif match == '172.21.22.181':
					#swap with randomIP
					line = line.replace(match, random.choice(randomIP))
					fout.write(line + "\n")
				else:
					continue
			else:
				fout.write(line + "\n")
