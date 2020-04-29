#This code is optional for reference on how to extract images using BeautifulSoup


import HTMLParser
from urllib.request import urlopen
import sys

urlString = "https://autoportal.com/upcoming-cars/"

def getImage(addr):
    u = urlopen(addr)
    data = u.read()

    splitPath = addr.split('/')
    fName = splitPath.pop()
    print (fName)

    f = open(fName, 'wb')
    f.write(data)
    f.close()

class parseImages(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name,value in attrs:
                if name == 'src':
                    getImage(urlString + "/" + value)

lParser = parseImages()

u = urlopen(urlString)
print (u.info())

lParser.feed(u.read())
lParser.close()




