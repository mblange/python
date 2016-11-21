#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

# Get MITRE page with techniques
res = requests.get("https://attack.mitre.org/wiki/All_Techniques")

# save the response
html_doc = res.text
#print doc

soup = BeautifulSoup(html_doc, 'html.parser')

headers = dict()

# Parse and establish table header dictionary (Name, Tactics, ID, Technical Description)
for header in soup.table.find_all('th'):
    headers[str(header.a.string)] = dict()

print headers

tactic = list()

for data in soup.table.find_all('tr'):
    if data:
        tactic = list.append(data.find_all(class_="Tactics")[0].a.string)
        print tactic
