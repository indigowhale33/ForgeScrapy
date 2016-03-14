from bs4 import BeautifulSoup
import requests
import urllib2
import re
import mechanize

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11 Firefox/14.0.1',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


url = 'http://sourceforge.net/directory/language:java/'

request = urllib2.Request(url,None, hdr)

br = mechanize.Browser()
br.set_handle_robots(False)
resp = br.open(request)

#print resp.read()
soup = BeautifulSoup(resp.read())


print soup.select('body')