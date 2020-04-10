from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from urllib.request import urljoin
import operator
from collections import Counter
from string import punctuation
import re

url = 'https://autoportal.com/upcoming-cars/'


app = Flask(__name__)

@app.route('/')
def index():
    data = []
    #images=[]
    source = requests.get('https://autoportal.com/upcoming-cars/').text

    soup = BeautifulSoup(source, 'lxml')
    
    #html = urlopen(url)
    #soup1 = BeautifulSoup(html,'html.parser')
    #dt = soup.find_all('img',attrs={'class':'lazy'})
    for a in soup.find_all('div',{'class':'cell4 cell-sm m_b-20'}):
        car_info = {}
        car_info['price']=a.find('span', attrs={'class':'price'}).text
        car_info['name'] = a.h3.text
        car_info['year'] = a.find('span',attrs={'class':'bold'}).text
        

        for b in soup.find_all('span',{'class':'img'}):
        
            car_info['image'] = b.find('img',attrs={'class':'lazy'}).get('data-original')
        for c in soup.find_all('div',{'class':'cell5 cell-sm m_b-20'}):
            car_info['ov']=c.find('div',{'class':'desc'})

        data.append(car_info)
        


    #for b in soup.find_all('div',{'class':'cell3 cell-sm m_b-20'}):
        #car_info['image'] = b.find_all('img',attrs={'class':'lazy'})
    
        #car_info['images'] = a.img.get("src")
        #link = soup.find(itemprop="img")
        #car_info['imgURL'] = a.select('img.lazy').('src')
        #car_info['imgURL'] =link["data-original"]
        #   data.append(car_info)
        #print(dt)
        #for b in soup.find_all('div',{'class':'cell3 cell-sm m_b-20'}):
        #car_info['image'] = b.find_all('img',attrs={'class':'lazy'})
        #data.append(car_info)
    
        
    return render_template('index.html',data=data)
@app.route('/more')
def home2():
    #data=[]
    source = requests.get('https://autoportal.com/upcoming-cars/').text

    soup = BeautifulSoup(source, 'lxml')
    output= soup.find('div',{'class':'cell4 cell-sm m_b-20'}).prettify()
    
    return render_template('more.html',output=output)


@app.route('/word')
def word():
     
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    text = (''.join(s.findAll(text=True))for s in soup.findAll('p'))

    c = Counter((x.rstrip(punctuation).lower() for y in text for x in y.split()))
    data1 = c.most_common()
    data2=[x for x in c if c.get(x) > 5]
    
    return render_template('word.html',data1=data1,data2=data2)    





if __name__ == '__main__': 
     app.run(debug=True)
