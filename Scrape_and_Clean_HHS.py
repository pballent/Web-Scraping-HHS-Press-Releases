# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:09:11 2019

@author: Phil Ballentine
"""
# Install packages if you need them
# pip install httplib2
# pip install BeautifulSoup
# pip install html2text
# pip install cssselect
# pip install pandas

import urllib2
import html2text
from bs4 import BeautifulSoup
import bleach
import lxml
import pandas
import re

## Getting the text from one URL

soup = BeautifulSoup(urllib2.urlopen('https://www.hhs.gov/about/news/2019/02/11/hhs-proposes-new-rules-improve-interoperability-electronic-health-information.html').read())
soup.get_text()
suba = str(soup.findAll('p'))
subb = suba.replace(',','') ## This helps it not break when doing csv conversion
subc = str(bleach.clean(subb, tags=[], strip=True)) ## Cleaning out all the html stuff, allow not tags, strip stuff
print(subc)

## Getting the scraped text data from the links on a webpage

File = urllib2.urlopen("http://www.hhs.gov/about/news/2018-news-releases/index.html")
Html = File.read()
File.close()

## Finding all the links on this HTML page denoted by <a> although some will be invalid
soup = BeautifulSoup(Html)
All = soup.find_all("a")

## Creating empty list to hold my URLs
list_urls = []

for links in All:
       list_urls.append('https://www.hhs.gov' + str(links.get('href')))
       
## Make list distinct by transmuting to set and back       
unique_list_urls = list(set(list_urls))

## Using a regex to match only the valid http addresses with only one https and one html and those that are actually press releases

p = re.compile('https{1}.*html{1}')
p2 = re.compile('.*2018+.*') ## this helps remove the generic URLs that aren't press releases
distinct_list_urls = unique_list_urls
clean_urls = [ s for s in distinct_list_urls if p.match(s) and p2.match(s) ]

keys = []
values = []
cleaned_values = []

for i in clean_urls:
    soup = BeautifulSoup(urllib2.urlopen(i).read())
    soup.get_text()
    suba = soup.findAll('p') ## Taking the <p> tagged items from the HTML
    subb = str(suba) ## Converting to string from ResultSet for the replace
    subc = subb.replace(',','') ## This helps it not break when doing csv conversion
    subd = bleach.clean(subc, tags=[], strip=True) ## Cleaning out all the html stuff, allow not tags, strip stuff
    keys.append(i)
    values.append(subc)
    cleaned_values.append(subd)

## Merging the url-value pairs into a dictionary that isn't really needed at this point but could be later
data = dict(zip(keys, cleaned_values)) 

## Merging them into a data frame and export to csv
pd = pandas.DataFrame({'col': keys})
pd['text'] = values
pd['clean_text'] = cleaned_values
pd.to_csv('hhs_press_releases_2018_2.csv', sep=',', encoding='utf-8')
