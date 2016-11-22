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

tactic = dict()
table = soup.find("table")
for row in table.findAll('tr')[0:]:
    col = row.findAll('td')
    Technique = str(col[0].string)
    Tactic = str(col[1].string)
    ID = str(col[2].string)
    description = str(col[3].string)

    record = (Technique, Tactic, ID, description)
    print "|".join(record)
