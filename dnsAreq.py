#!/usr/bin/env python
import dns.resolver
import os,binascii
from time import sleep

# Create new dns resolveer instance
resolver = dns.resolver.Resolver()
# All requested domains are bogus so don't wait around
resolver.timeout = .5
resolver.lifetime = .5

# Make 100 DNS 'A' record requests
for d in range(0, 100):
    domain = str()
    # Create two 16 byte hex subdomains
    sd1 = binascii.b2a_hex(os.urandom(16)) + '.'
    sd2 = binascii.b2a_hex(os.urandom(16)) + '.'
    # Prepend them to 'cyberpewpew.lol'
    domain = sd1 + sd2 + 'cyberpewpew.lol'
    # Make DNS 'A' record request
    try:
        print 'attempt #:  %d' %d
        print 'To: %s' %domain
        ans = resolver.query(domain, "A")
        # Wait one second to mimic real requests timing
        sleep(.5)
    except Exception as e: 
        print str(e)
