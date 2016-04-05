#!/usr/bin/env python
## a tool for identifying vulnerable JBoss Application Servers.
## Author: Matt Lange
## Date: 3/31/2016

import threading
import requests
from netaddr import *
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
import argparse

RED = '\x1b[91m'
GREEN = '\033[32m'
ENDC = '\033[0m'

# parse arguments
ap = argparse.ArgumentParser(description='This is a jboss vulnerability scanner. You could also just use Metasploit...')
ap.add_argument('target', type=str, help='CIDR notation or ip address', default=None)
ap.add_argument('--ports', '-p', type=str, help='an nmap-stlye, comma-separated list of ports to scan', default='80,8080,8008,8000')
ap.add_argument('--log', '-l',  help='write results to LOG', default='log_jBoss.txt')
args = ap.parse_args()

# validate target argument is a valid IP address
try:
	IPNetwork(args.target)
except:
	print '-' *60
	print(RED + 'You entered an invalid IP address %s' %args.target + ENDC)
	print '-' *60
	ap.print_help()
	exit()

# define ports to scan
ports = args.ports

# define vulnerable requests
paths = ["/web-console/Invoker","/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.system:type=ServerInfo","/web-console/ServerInfo.jsp","/invoker/JMXInvokerServlet"]

# create empty webServers list
webServers = []

#define a logging function
def log(url, status):
	with open(args.log, 'a') as log:
		if status:
			log.write(GREEN + "[*] OK [*] %s\n" %(url) + ENDC)
		else:
			log.write(RED + "[*] VULNERABLE [*] %s\n" %(url) + ENDC)

# scan for open web servers
def portScan():
	global parsed
	print"Scanning ports: %s" %ports
	nm = NmapProcess(args.target, options="-sS -n -T4 -p%s" %ports)
	rc = nm.run()
	if rc != 0:
		print("nmap scan failed: {0}".format(nm.stderr))
	parsed = NmapParser.parse(nm.stdout)

def makeURL():
	for host in parsed.hosts:
		for service in host.services:
			if service.open():
				for path in paths:
					webServers.append("%s:%s%s" % (host.address, service.port, path))
# attempt at comprehension. 
# webServers = [str(host.address) + ':' + str(service.port) + str(path) for host in parsed.hosts for service in host.services if service.open() for path in paths ]

# thread vulnCheck
def vCheck():
	Thread = threading.Thread
	for url in webServers:
		while 1:
			if threading.activeCount() <= 10:
				t = Thread(target=vulnCheck, args=(url,))
				t.start()
				break

# request vulnerable pages
def vulnCheck(url):
	r = requests.get('http://'+url,timeout=5,allow_redirects=False,verify=False)
	status = r.status_code
	if status == 200 or status == 500:
		print(RED + "[*] VULNERABLE [*] %s" % url + ENDC)
		log(url, 0) 
	else:
		print(GREEN + "[+] OK: %s" % url + ENDC)
		log(url, 1) 

def main():
	portScan()
	makeURL()
	vCheck()

if __name__ == '__main__':
    main()
