#!/usr/bin/python 
# -*- coding: utf8 -*-
from wikitools import wiki                                                                                                                                                          
from wikitools import api                                                                                                                                                           
from wikitools import page
from wikitools import wikifile
# create a Wiki object                                                                                                                                                              
site = wiki.Wiki("http://mediawiki.loc/api.php")                                                                                                                                

site.login('Wikiadmin', 'gfhjkm', True)

page = page.Page(site=site, title='Test page')
page.edit(newtext='new text [[Категория:Лайя йога]] [[Категория:%s]]'%('книга тайны'));

file = wikifile.File(wiki=site, title='new file.pdf')
print file.upload(fileobj=open('pdf/t.pdf'), ignorewarnings=True, watch=True )

# define the params for the query                                                                                                                                                   
params = {'action':'query', 'titles':'Test page' }
# create the request object                                                                                                                                                         
request = api.APIRequest(site, params)                                                                                                                                              
# query the API                                                                                                                                                                     
result = request.query()  

print result
