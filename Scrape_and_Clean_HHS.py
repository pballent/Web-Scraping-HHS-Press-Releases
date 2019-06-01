# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:09:11 2019

@author: Phil Ballentine
"""

##getting the text from one URL
import urllib2
import html2text
from bs4 import BeautifulSoup

soup = BeautifulSoup(urllib2.urlopen('https://www.hhs.gov/about/news/2019/02/11/hhs-proposes-new-rules-improve-interoperability-electronic-health-information.html').read())

soup.get_text()

subc = soup.findAll('p')

print(subc)

##Getting the scraped text data from the links on a webpage
##finding all html links on a particular webpage
from bs4 import BeautifulSoup
import urllib2

File = urllib2.urlopen("http://www.hhs.gov/about/news/2018-news-releases/index.html")
Html = File.read()
File.close()
##Finding all the links on this HTML page denoted by <a> although some will be invalid
soup = BeautifulSoup(Html)
All = soup.find_all("a")

##Creating empty list to hold my URLs
z = []

for links in All:
       z.append('https://www.hhs.gov' + str(links.get('href')))
       
##Make list distinct by transmuting to set and back       
z_set = list(set(z))


##Using a regex to match only the valid http addresses with only one https and one html
import re

p = re.compile('https{1}.*html{1}')
p2 = re.compile('.*2018+.*') ##this helps remove the generic URLs that aren't press releases
l1 = z_set
l2 = [ s for s in l1 if p.match(s) and p2.match(s) ]


import urllib2
import html2text
from bs4 import BeautifulSoup
import bleach

keys = []
values = []
values2 = []

for i in l2:
    soup = BeautifulSoup(urllib2.urlopen(i).read())
    soup.get_text()
    subc = soup.findAll('p') #taking the <p> from the HTML
    subd = str(subc) #converting to string from ResultSet for the replace
    sube = subd.replace(',','') #this helps it not break when doing csv conversion
    ##cleaning out all the html stuff, allow not tags, strip stuff
    subf = bleach.clean(sube, tags=[], strip=True)
    keys.append(i)
    values.append(sube)
    values2.append(subf)

## merging the url-value pairs into a dictionary that isn't really needed at this point but could be later
data = dict(zip(keys, values2)) 
##printing results
   

##merging them into a data frame
 pd = pandas.DataFrame({'col': keys})
 pd['col2'] = values
 pd['col3'] = values2
 pd.to_csv('pd_ouput3.csv', sep=',', encoding='utf-8')

