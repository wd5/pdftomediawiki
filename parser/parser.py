# -*- coding: utf8 -*-

import os
import re
import sys

from wikitools import wiki
from wikitools import api
from wikitools import page
from wikitools import wikifile

pdftohtml = '/usr/bin/pdftohtml'
tmpdir = 'html'
htmlname = 's'
api_url = 'http://mediawiki.loc/api.php'

class Parser(object):

    def __init__(self, book, file, startpage, endpage):
        self.book = book
        self.start = startpage
        self.end = endpage
        self.filename  = file
        self.file = ''
        self.intro = ''

        try:
            open(file)
        except:
            sys.exit("Error in open file %s" % file)

        self.site = wiki.Wiki(api_url)
        self.logged = False
        self.login()


    def pdftohtml(self):
        try:
            os.system('%s "%s" "%s/%s.html"' % (pdftohtml, self.filename,  tmpdir, self.book))
            self.fhandle = open('%s/%ss.html' % (tmpdir, self.book))
        except:
            sys.exit("Error in conver or open converted file %s/%ss.html" % (tmpdir, self.book))

        self.getdata()

    def login(self):
        self.logged = self.site.login('Wikiadmin', 'gfhjkm', True)
        if self.logged is False:
            sys.exit('login failed')

    def getdata(self):
        i = 1
        #start = 8
        #end = 43
        try:
            for line in self.fhandle:

                if line.find('<hr>') != -1:
                    i += 1
                if i < self.end:
                    if i >= self.start:
                        self.file += line.replace('&nbsp;', ' ').replace('-<br>\n', '')
                    else:
                        self.intro += line.replace('&nbsp;', ' ').replace('-<br>\n', '')
        finally:
            self.fhandle.close()

        self.file = re.sub('<A name=\d+></a>', '', self.file)
        self.intro = re.sub('<A name=\d+></a>', '', self.intro)
        self.file = re.sub('<i><b>\d+</b></i><br>\n', '', self.file)
        self.intro = re.sub('<i><b>\d+</b></i><br>\n', '', self.intro)

    def title(self, title):
        return re.sub('<[^>]+?>','', title.replace('\n', '').replace('»', '').replace('«','')).strip().lower()

    def html2wikimarkup(self, text):
        text = re.sub('<IMG src="%s/([^"]+)">'%tmpdir, '[[Файл:\\1|thumb]]',  text)
        text.replace('<i>', "''").replace('</i>', "''")
        return re.sub('<[^>]+?>','', text.replace('<b>', '== ').replace('</b>', ' ==').replace('&nbsp;', ''))

    def createbook(self):


        i = re.compile('<img src="(?P<source>[^"]+)">', re.I)
        images = i.findall(self.intro)
        self.intro = self.html2wikimarkup(self.intro)

        self.login()

        file = wikifile.File(wiki=self.site, title=self.book + '.pdf')
        f = open(self.filename)
        fileout = file.upload(fileobj=f, watch=True, ignorewarnings=True, comment="Парсинг из книги %s" % self.book)
        page1 = page.Page(site=self.site, title='Файл:%s%s' % (self.book, '.pdf'))
        page1.edit(newtext='%s [[Категория:Лайя йога]] [[Категория:%s]]'%(self.intro, self.book))
        print "Book = Файл:%s, [[Категория:%s]]" % (self.book + '.pdf', self.book)

        for image in images:
            filename = image.replace('html/', '')
            file = wikifile.File(wiki=self.site, title=filename)
            file.upload(fileobj=open(image), watch=True, ignorewarnings=True, comment="Парсинг из книги %s" % self.book)
            page1 = page.Page(site=self.site, title='Файл:%s' % filename)
            page1.edit(newtext='Иллюстрация из книги [[Категория:%s]]'%(self.book))
            print "Image = Файл:%s" % (image)

    def createpages(self):

        # Лайя йога в традиции сиддхов
        # p = re.compile('((?P<title><i><b>[абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ—«».,\s-]+</b></i><br>\n){1,5})(?P<text>.*?)Глава [A-Z0-9\s]+</b>', re.S | re.I)
        
        # Путь божественной гордости
        """
        p = re.compile('((?P<title><i><b>[абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ—«».,\s-]+</b></i><br>\n){1,5})(?P<text>.*?)<i><b>', re.S | re.I)
        links = p.findall(self.file)
        i = re.compile('<img src="(?P<source>[^"]+)">', re.I)
        images = i.findall(self.file)
        """

        self.file = re.sub(pattern = '(<i><b>([абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ—«».,\s-]+)</b></i><br>\n)', repl =  '<title> \\2</title>\n', string = self.file )
        self.file = re.sub(pattern = '</title>\n.*<title>', repl =  '', string = self.file )
        data = self.file.split('<title>');

        self.login()
        page_count = 0;

        for d in data:
            title_index = d.find('</title>')

            if title_index != -1:
                text = d[title_index+8:d.__len__()]
                page1 = page.Page(site=self.site, title='%s' % self.title(d[0:title_index]))
                page1.edit(newtext='%s [[Категория:Лайя йога]] [[Категория:%s]]' % (self.html2wikimarkup(text), self.book))
                print "Page = %s, info: %s" % (self.title(d[0:title_index]), self.html2wikimarkup(text)[:10])
                page_count += 1;

                i = re.compile('<img src="(?P<source>[^"]+)">', re.I)
                images = i.findall(text)

                for image in images:
                    filename = image.replace('html/', '')
                    file = wikifile.File(wiki=self.site, title=filename)
                    file.upload(fileobj=open(image), watch=True, ignorewarnings=True, comment="Парсинг из книги %s" % self.book)
                    page1 = page.Page(site=self.site, title='Файл:%s' % filename)
                    page1.edit(newtext='Иллюстрация из книги [[Категория:%s]]'%(self.book))
                    print "Image = Файл:%s" % (image)
                    print 'Image = ' + image
            else:
                print "Not a page = %s, info: %s, index: %d" % (self.title(d[0:10]), self.html2wikimarkup(d)[10:100], title_index)


        print "Загруженно страниц: %d " % page_count            

    def __del__(self):
        os.system('rm -rf %s/*' % tmpdir )
