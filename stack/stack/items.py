# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class StackItem(Item):
	title= Field()
	url= Field()      #website url
	stars= Field()    #overall star
	downloads=Field() #number of downloads in this week 
	categories=Field()
	licenses=Field()  #current licenses
	clone=Field()     # git/svn clone url(in form of git clone http://....)
	navmenu = Field() # nav menu items
	tickets = Field() # tickets url
	reviews = Field() # reviews url

	def keys(self):
		return ['title', 'url', 'stars', 'downloads', 'categories', 'licenses','clone',
		'tickets', 'reviews']
