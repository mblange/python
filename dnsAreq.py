#!/usr/bin/env python
import sys
import dns.resolver
import os,binascii
from time import sleep

# Accept a number of requests to make if given, else, 100
if len(sys.argv) > 1:
    num = sys.argv[1]
else:
    num = 100

# Accept a domain name, else, cyberpewpew.lol
if len(sys.argv) > 2:
    domain = sys.argv[2]
else:
    domain = 'cyberpewpew.lol'

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
    # Prepend them to 'cyberpewpew.lol'
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
