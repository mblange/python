#!/usr/bin/env python
# Create new resolveer instance
import dns.resolver
import random
import string
import os,binascii

# Create new resolveer instance
myRes = dns.resolver.Resolver()

for d in range(0, 100):
    domain = str()
    #sD1 = str()
    #sD2 = str()
    # Create random domain name
    #for i in range(4):
    #    s = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)) + '.'
    #    subDomain += s
    #sD1 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16)) + '.'
    #sD2 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(162)) + '.'
    sd1 = binascii.b2a_hex(os.urandom(16)) + '.'
    sd2 = binascii.b2a_hex(os.urandom(16)) + '.'
    domain = sd1 + sd2 + 'cyberpewpew.lol'
    print d
    print domain
'''
    try:
        myAns = myRes.query(domain, "A")
    except:
        continue
'''
