#   
# TODO
#   - Figure out how to transmore HTML codes to characters:
#   - [[URGENT]] Instead of dumping to console, return data as variables!       

import formatter, htmllib, os, StringIO, zipfile
#import base64, webbrowser, re, readline, tempfile, locale

from bs4 import BeautifulSoup

#locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
basedir = ''

def check_epub(fl):
    '''
    Check if fl is a file and ends in ".epub" 
    '''
    if os.path.isfile(fl) and os.path.splitext(fl)[1].lower() == '.epub':
        return True

def open_epub(fl):
    if not check_epub(fl):
        print 'File ' + fl + ' was not found'
        return None

    return zipfile.ZipFile(fl, 'r')
    print 'found!'

def dump_epub(fl, maxcol=float("+inf")):
    '''
    Dump the contents of the EPUB file as text
    '''
    if not check_epub(fl):
        return
    fl = zipfile.ZipFile(fl, 'r')
    chaps = [i for i in table_of_contents(fl)]
    for title, src in chaps:
        print title
        print '-' * len(title)
        if src:
            soup = BeautifulSoup(fl.read(src))
            print textify(
                unicode(soup.find('body')).encode('utf-8'),
                maxcol=maxcol,
            )
        #print '\n'

def table_of_contents(fl):
    global basedir

    # find opf file
    soup = BeautifulSoup(fl.read('META-INF/container.xml'))
    opf = dict(soup.find('rootfile').attrs)['full-path']

    basedir = os.path.dirname(opf)
    if basedir:
        basedir = '{0}/'.format(basedir)

    soup =  BeautifulSoup(fl.read(opf))

    # title
    # yield (soup.find('dc:title').text, None)

    # all files, not in order
    x, ncx = {}, None
    for item in soup.find('manifest').findAll('item'):
        d = dict(item.attrs)
        x[d['id']] = '{0}{1}'.format(basedir, d['href'])
        if d['media-type'] == 'application/x-dtbncx+xml':
            ncx = '{0}{1}'.format(basedir, d['href'])

    # reading order, not all files
    y = []
    for item in soup.find('spine').findAll('itemref'):
        y.append(x[dict(item.attrs)['idref']])

    z = {}
    if ncx:
        # get titles from the toc
        soup =  BeautifulSoup(fl.read(ncx))

        for navpoint in soup('navpoint'):
            k = navpoint.content.get('src', None)
            # strip off any anchor text
            k = k.split('#')[0]
            if k:
                z[k] = navpoint.navlabel.text

    # output
    for section in y:
        if section in z:
            yield (z[section].encode('utf-8'), section.encode('utf-8'))
        else:
            yield (u'', section.encode('utf-8').strip())

def textify(html_snippet, img_size=(80, 45), maxcol=72):
    ''' Text dump of HTML Document '''
    class Parser(htmllib.HTMLParser):
        def anchor_end(self):
            self.anchor = None
        def handle_image(self, source, alt, ismap, alight, width, height):
            global basedir
            self.handle_data(
                '[img="{0}{1}" "{2}"]'.format(basedir, source, alt)
            )

    class Formatter(formatter.AbstractFormatter):
        pass

    class Writer(formatter.DumbWriter):
        def __init__(self, fl, maxcol=72):
            formatter.DumbWriter.__init__(self, fl)
            self.maxcol = maxcol
        def send_label_data(self, data):
            self.send_flowing_data(data)
            self.send_flowing_data(' ')

    o = StringIO.StringIO()
    p = Parser(Formatter(Writer(o, maxcol)))
    p.feed(html_snippet)
    p.close()

    return o.getvalue()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("book", help="Load the book.");
    args = parser.parse_args()
    dump_epub(args.book)