#!/usr/bin/python
# -*- coding: utf8 -*-
from wikitools import wiki                                                                                                                                                          
from wikitools import api                                                                                                                                                           
from wikitools import page
from wikitools import wikifile
# create a Wiki object                                                                                                                                                              
site = wiki.Wiki("http://mediawiki.loc/api.php")                                                                                                                                

site.login('Wikiadmin', 'gfhjkm', True)

# page1 = page.Page(site=site, title='Test page')
# page1.edit(newtext='new text [[Файл:1.png|thumb]][[Категория:Лайя йога]] [[Категория:%s]]'%('книга тайны'))

file = wikifile.File(wiki=site, title='111.pdf')
print file.upload(fileobj=open('1.pdf'), watch=True )

page2 = page.Page(site=site, title='Файл:111.pdf')
page2.edit(newtext='[[Категория:Лайя йога]] [[Категория:%s]]'%('книга тайны'));

"""
# define the params for the query                                                                                                                                                   
params = {'action':'query', 'titles':'Test page' }
# create the request object                                                                                                                                                         
request = api.APIRequest(site, params)                                                                                                                                              
# query the API                                                                                                                                                                     
result = request.query()  


print result
"""
