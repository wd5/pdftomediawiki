
"""
#!/usr/bin/python
# -*- coding: utf8 -*-

f = open("html/ss.html")

file  = ''

i = 0
try:
    for line in f:
        file += line

finally:
    f.close()

p = re.compile('<a name=[^>]+></a><b>(?P<name>Глава.+)</b><br>\n((<i><b>.+</b></i><br>\n){1,3})', re.I)
links = p.findall(file)
print links

for link in links:
    print re.sub('<[^>]+?>', '', link[0] + ' ' + link[1]).replace('&nbsp;', '')


page = file.split('<hr>')

end = 8

for index in range(0,7):
    print re.sub('<[^>]+?>', '', page[index]).replace('&nbsp;', '')
    """
    

