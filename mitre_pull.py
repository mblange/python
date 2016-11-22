#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import lxml
import csv

# Get MITRE page with techniques, save response, and parse
res = requests.get("https://attack.mitre.org/wiki/All_Techniques")
html_doc = res.text
soup = BeautifulSoup(html_doc, 'lxml')

# establish list
csv_out = list()

# Parse and establish table headers (Name, Tactics, ID, Technical Description)
headerList = list()

for header in soup.table.find_all('th'):
    headerList.append(str(header.a.string))

csv_out.append(headerList)

# Parse and establish table data (Name, Tactics, ID, Technical Description)
table = soup.find("table")
for row in table.findAll('tr')[0:]:
    col = row.findAll('td')
    Technique = str(col[0].string).replace('\n', '')
    Tactic = str(col[1].get_text(", ")).replace('\n', '')
    ID = str(col[2].string).replace('\n', '')
    Description = str(col[3].get_text(" ")).replace('\n', '')
    record = [Technique, Tactic, ID, Description]
    csv_out.append(record)

with open('mitre_attack.csv', "wb") as out_file:
    wr = csv.writer(out_file, dialect='excel')
    wr.writerows(csv_out)
