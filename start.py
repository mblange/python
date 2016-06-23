#!/usr/bin/env python

###################################
# Template to thread http requests
###################################

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import requests

urls = [
  'http://www.python.org', 
  'http://www.python.org/about/',
  'http://www.python.org/download/',
  'https://wiki.python.org/moin/',
  'http://planet.python.org/',
  'http://www.python.org/psf/',
  'http://www.python.org/community/awards/'
  ]

# create function using 'requsts' module to GET 'urls'
def req(url):
	r = requests.get(url)
	return r

############# Threading ######################
# Make the Pool of workers
pool = ThreadPool(8) # Sets the pool size to 8

# Open the urls in their own threads and return list
results = pool.map(req, urls)

# Close the ppol and wait for the work to finish
pool.close()
pool.join()
############# Threading ######################

print results[0].url
for i in results:
	print i.url, i.status_code #.headers, .cookies, .history 
