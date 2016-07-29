#!/usr/bin/env python

#####################
# defeat anti-csrf tokens
#####################

try:
	import requests
	import lxml.html as lh
	from io import StringIO
except ImportError, e:
	print "Exception: {}".format(str(e))
	exit(1)

# establish vars
url = 'http://127.0.0.1:8000/'
token_header = 'Content-type'
data = {}

# establish session
s = requests.Session()

# make initial request to get token
r = s.get(url)

#print(r.text)
#token = r.headers[token_header]
tree = lh.fromstring(r.content)
html = tree.xpath('//a[@href]/text()')
print html
# make second request with token
