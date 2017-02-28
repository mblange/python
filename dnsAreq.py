#!/usr/bin/env python
import dns.resolver
import os,binascii

# Create new dns resolveer instance
myRes = dns.resolver.Resolver()

# Make 100 DNS 'A' record requests
for d in range(0, 100):
    domain = str()
    # Create two 16 byte hex subdomains
    sd1 = binascii.b2a_hex(os.urandom(16)) + '.'
    sd2 = binascii.b2a_hex(os.urandom(16)) + '.'
    # Prepend them to 'cyberpewpew.lol'
    domain = sd1 + sd2 + 'cyberpewpew.lol'
    # For troubleshooting...
    print d
    print domain
'''
    # Make DNS 'A' record request
    try:
        myAns = myRes.query(domain, "A")
    except:
        continue
'''
