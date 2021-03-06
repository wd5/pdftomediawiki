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
api_url = 'http://wikidharma.com/api.php'
# api_url = 'http://mediawiki.loc/api.php'

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
            # os.system('%s "%s" "%s/%s.html"' % (pdftohtml, self.filename,  tmpdir, self.book))
            self.fhandle = open('%s/%ss.html' % (tmpdir, self.book))
        except:
            sys.exit("Error in conver or open converted file %s/%ss.html" % (tmpdir, self.book))

        self.getdata()

    def login(self):
        self.logged = self.site.login('Wikiadmin', '9MdVYsp', True)
        # self.logged = self.site.login('Wikiadmin', 'gfhjkm', True)
        if self.logged is False:
            sys.exit('login failed')

    def getdata(self):
        i = 1
        #start = 8
        #end = 43
        try:
            for line in self.fhandle:

                # line = line.decode('utf8').encode('cp1251').decode('cp1251')
                if line.find('<hr>') != -1:
                    i += 1
                if i < self.end:
                    if i >= self.start:
                        self.file += line.replace('&nbsp;', ' ').replace('-<br>\n', '')
                    else:
                        self.intro += line.replace('&nbsp;', ' ').replace('-<br>\n', '')
        finally:
            self.fhandle.close()


    def title(self, title):
        return re.sub('<[^>]+?>','', title.replace('\n', '').replace('»', '').replace('«','')).strip().lower()

    def html2wikimarkup(self, text):
        text = re.sub('<IMG src="%s/([^"]+)">'%tmpdir, '[[Файл:\\1|thumb]]',  text)
        text.replace('<i>', "''").replace('</i>', "''")
        return re.sub('<[^>]+?>','', text.replace('<b>', '== ').replace('</b>', ' ==\n').replace('&nbsp;', '')).strip()

    def createbook(self):


        i = re.compile('<img src="(?P<source>[^"]+)">', re.I)
        images = i.findall(self.intro)
        self.intro = self.html2wikimarkup(self.intro)

        self.login()

        """
        self.intro = re.sub('<A name=\d+></a>', '', self.intro)
        self.intro = re.sub('<i><b>\d+</b></i><br>\n', '', self.intro)
        """

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
        
        self.file = re.sub(pattern = '(<i><b>([абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ—«».,\s-]+)</b></i><br>\n)', repl =  '<title> \\2</title>\n', string = self.file )
        self.file = re.sub(pattern = '</title>\n.*<title>', repl =  '', string = self.file )

        self.file = re.sub(pattern = '(<A name=\d+></a>)(<IMG .*)\n(.*<br>\n.*)<br>', repl =  '\\1\\3<br>\n \2<br>', string = self.file )
        self.file = re.sub(pattern = '<A name=\d+></a>Глава[0-9A-Za-z\s]+(.*?)<b>', repl =  '<title> \\1</title>\n', string = self.file, flags=re.S )

        self.file = re.sub(pattern = '</title>\n.*<title>', repl =  '', string = self.file )
        data = self.file.split('<title>');

        self.login()
        page_count = 0;

        for d in data:

            slice = d.split('</title>');

            try:
                title = slice[0]
                text = slice[1]
                print "Page = %s, info: %s" % (self.title(title), self.html2wikimarkup(text)[:100])
                page1 = page.Page(site=self.site, title='%s' % self.title(title))
                page1.edit(skipmd5 = True, newtext='%s [[Категория:Лайя йога]] [[Категория:%s]]' % (self.html2wikimarkup(text), self.book))
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
            except IndexError:
                print "Not a page = %s " % (self.title(slice[0]) )


        print "Загруженно страниц: %d " % page_count            

    #def __del__(self):
    # os.system('rm -rf %s/*' % tmpdir )
