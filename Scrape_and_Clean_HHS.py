# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:09:11 2019

@author: Phil Ballentine
"""
# Install packages
# pip install httplib2
# pip install BeautifulSoup
# pip install html2text
# pip install cssselect

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


##Using a regex to match only the valid http addresses with only one https and one html and those that are actually press releases
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
    subc = soup.findAll('p') ## Taking the <p> from the HTML
    subd = str(subc) ## Converting to string from ResultSet for the replace
    sube = subd.replace(',','') ## Remove commas from the text so it doesn't break when doing csv conversion
    subf = bleach.clean(sube, tags=[], strip=True)  ##Cleaning out all the html stuff, allow no tags, strip HTML-y stuff
    keys.append(i)
    values.append(sube)
    values2.append(subf)

## Merging the url-value pairs into a dictionary that isn't really needed at this point but could be later
dictionary_of_url_and_text = dict(zip(keys, values2)) 
   

## Merging them into a data frame
pd = pandas.DataFrame({'col': keys})
pd['text'] = values
pd['clean_text'] = values2
pd.to_csv('hhs_press_releases_2018.csv', sep=',', encoding='utf-8')

