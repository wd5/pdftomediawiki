# -*- coding: utf8 -*-
from parser import  parser

#p = parser.Parser('Лайя йога в традиции сиддхов', 'pdf/t.pdf', 8, 43)
# p = parser.Parser('Путь божественной гордости', 'pdf/way_of_god_beuaty.pdf', 13, 154)
p = parser.Parser('Путь эволюции', 'pdf/evolution_way.pdf', 10, 61)
p.pdftohtml()
p.createbook()
p.createpages()
