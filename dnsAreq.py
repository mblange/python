#!/usr/bin/env python
# Create new resolveer instance
import dns.resolver
import random
import string

# Create new resolveer instance
myRes = dns.resolver.Resolver()

for d in range(0, 100):
    domain = str()
    subDomain = str()
    # Create random domain name
    for i in range(4):
        s = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32)) + '.'
        subDomain += s
    domain = subDomain + 'cyberpewpew.lol'
    print d
    print domain

    try:
        myAns = myRes.query(domain, "A")
    except:
        continue
