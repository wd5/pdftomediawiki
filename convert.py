#!/usr/bin/python2.7
# -*- coding: utf8 -*-
import re,sys
# import locale
# locale.setlocale(locale.LC_ALL, "")

f = open("html/ss.html")

file  = ''
intro = ''

i = 1 
start = 10 
end =  61
try:
    for line in f:

        if line.find('<hr>') != -1:
            i += 1
        if i < end: 
            if i >= start:
                file += line
            else:
                intro += line
finally:
    f.close()

# file = file.replace("Драгоценные наставления&nbsp;&nbsp;<br>", '').replace('о пестовании Истинной Природы<br>', '').replace('<i><b>Свабхава&nbsp;Упадеша&nbsp;&nbsp;</b></i><br>', '').replace('<i><b>Чинтамани</b></i><br>', '');   
file = file.replace('&nbsp;', ' ').replace('-<br>\n', '');
file.replace('-<br>\n', '');

file = re.sub(pattern = '<A name=\d+></a>Глава[0-9A-Za-z\s]+(.*?)<b>', repl =  '<title> \\1</title>\n', string = file, flags=re.S )

file = re.sub(pattern = '</title>\n.*<title>', repl =  '', string = file )
data = file.split('<title>');

for d in data:
    title_index = d.find('</title>')
    print 'title' + d[0:title_index]
    text = d[title_index+8:d.__len__()]
    print 'text' + text[:50]

    i = re.compile('<img src="(?P<source>[^"]+)">', re.I)
    images = i.findall(text)

    for image in images:
        print 'Image = ' + image

print file
sys.exit(0);


p = re.compile('((?P<title><i><b>[НираламбхаабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ()—«».,\s-]+</b></i><br>\n){1,5})(?P<text>.*?)<i><b>', re.S | re.I)
# p = re.compile('((?P<title><i><b>[НираламбхаабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ—«».,\s-]+</b></i><br>\n){1,5})(?P<text>.*?)(<hr>\n|<i><b>)', re.S | re.I)
#p = re.compile('((<i><b>[ а-яА-ЯёЁ0-9\-_\t]+</b></i><br>\n){1,3})', re.S | re.I | re.L)
# p = re.compile('((<i><b>[абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ—«».,\s-]+</b></i><br>\n){1,6})', re.S | re.I )
links = p.findall(file)
i = re.compile('<img src="(?P<source>[^"]+)">', re.I)
images = i.findall(file)

def title(title):
    return re.sub('<[^>]+?>','', title.replace('\n', '').replace('»', '').replace('«',''), re.I).strip().lower()

def html2wikimarkup(text):
    text = re.sub('<IMG src="([^"]+)">', '[[Файл:\\1|thumb]]',  text)
    text.replace('<i>', "''").replace('</i>', "''")
    return re.sub('<[^>]+?>','', text.replace('<b>', ' == ').replace('</b>', ' == ').replace('&nbsp;', ''))

i = 0;
for link in links:
    i += 1
    print "%d %s" %(i, title(link[0]))
#    print html2wikimarkup(link[2])[:25]
print "\n"

# print links.__len__()
# print html2wikimarkup(intro)
# print images

# for index in range(0,7):
#    print re.sub('<[^>]+?>', '', page[index]).replace('&nbsp;', '')
