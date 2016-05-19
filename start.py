#!/usr/bin/env python

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import requests

# Threading
urls = [
  'http://www.python.org', 
  'http://www.python.org/about/',
  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'https://wiki.python.org/moin/',
  'http://planet.python.org/',
  'https://wiki.python.org/moin/LocalUserGroups',
  'http://www.python.org/psf/',
  'http://www.python.org/community/awards/'
  ]

# create function using requst module to GET 'urls'
def req(url):
	r = requests.get(url)
	return r

# Make the Pool of workers
pool = ThreadPool(4) # Sets the pool size to 4

# Open the urls in their own threads and return the results
results = pool.map(req, urls)

# Close the ppol and wait for the work to finish
pool.close()
pool.join()

print results[0].status_code
print results[0].headers
print results[0].cookies
print results[0].history
print results[0].url
for i in results:
	print i.url
