## scan for jboss
import threading
import requests
from netaddr import *
from sys import argv
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
import argparse

__version__ = "0.1"

RED = '\x1b[91m'
GREEN = '\033[32m'
ENDC = '\033[0m'

# parse arguments
ap = argparse.ArgumentParser(description='crappy "jexboss" vulnerability scanner v%s' % (__version__))
group = ap.add_mutually_exclusive_group()
ap.add_argument('network', help='CIDR notation of network to scan', default=None)
group.add_argument('--ip', help='ip to scan', default=None)
args = ap.parse_args()

#define a logging function (or class?)
def log(url):
	with open('scan_log.txt', 'a') as log:
		 log.write("[*] VULNERABLE [*]%s\n" %(url))

# accept and parse cidr
srvs = []
if args.ip:
	srvs.append(args.ip)
else:
	for net in IPNetwork(args.network).iter_hosts():
		srvs.append(net)
servers = [str(ip) for ip in srvs ]
ports = '80,8080,8008,8000'

# scan for open web servers
def portScan():
	for server in servers:
		nm = NmapProcess(server, options="-sS -n -T4 -p%s" %ports)
		rc = nm.run()
		if rc != 0:
			print("nmap scan failed: {0}".format(nm.stderr))
		parsed = NmapParser.parse(nm.stdout)
		for host in parsed.hosts:
			for service in host.services:
				if service.open():
					for path in paths:
						webServers.append("%s:%s%s" % (host.address, service.port, path))
webServers = []
paths = ["/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.system:type=ServerInfo","/web-console/ServerInfo.jsp","/invoker/JMXInvokerServlet"]
	
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
	r = requests.get('http://'+url,timeout=5)
	status = r.status_code
	if status == 200 or status == 500:
		print(RED + "[*] VULNERABLE [*] %s" % url + ENDC)
		log(url)
	else:
		print (GREEN + "[+] OK: %s" % url + ENDC)
portScan()
vCheck()
