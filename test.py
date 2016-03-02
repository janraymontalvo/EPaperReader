import zipfile, os
from bs4 import BeautifulSoup

import epub

fl = zipfile.ZipFile('zipfile.epub', 'r') # test.epub = epub file name
soup = BeautifulSoup(fl.read('META-INF/container.xml'))
# opf = dict(soup.find('rootfile').attrs)['full-path']

# basedir = os.path.dirname(opf)
# if basedir:
# 	basedir = '{0}/'.format(basedir)

# soup =  BeautifulSoup(fl.read(opf))
# print soup.find('dc:title').text # title
# print soup.find('dc:creator').text #author

# chaps = list([i for i in epub.table_of_contents(fl)]) # List of links to chapters index 0 is the title
# print chaps

soup = BeautifulSoup(fl.read('OEBPS/chap1-03.xhtml'))
print soup.learn.q1.text
# for i in chaps:
# 	print i[1]
# # chaps = [i for i in epub.table_of_contents(fl)]
# # print chaps

