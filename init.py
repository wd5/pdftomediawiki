# -*- coding: utf8 -*-
from parser import  parser

# p = parser.Parser('Лайя йога в традиции сиддхов', 'pdf/t.pdf', 8, 43)
p = parser.Parser('Путь божественной гордости', 'pdf/pyt.pdf', 13, 154)
p.pdftohtml()
p.createbook()
p.createpages()
