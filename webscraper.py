from flask import Flask, render_template,request,make_response,redirect,url_for
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from urllib.request import urljoin
from collections import Counter
from string import punctuation
import re
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import *


url = 'https://autoportal.com/upcoming-cars/'


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class customer(db.Model):
    firstname = db.Column('firstname',db.String(20),nullable=False,primary_key=True)
    lastname  = db.Column('lastname',db.String(20),nullable=True)
    country = db.Column('country',db.String(15))
    category = db.Column('category',db.String(15))
    contact = db.Column('contact',db.Integer)
    def __init__(self,firstname,lastname,country,category,contact):
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.category = category
        self.contact = contact
        
        
class CustomerForm(Form):
    firstname = StringField('firstname', validators=[validators.required(), validators.Length(min=6, max=20)])
    lastname = StringField('lastname', validators=[validators.required(), validators.Length(min=6, max=20)])
    country = StringField('country', validators=[validators.required()])
    category = StringField('country', validators=[validators.required()])
    contact = StringField('contact')


@app.route('/')
def home():
    source = requests.get('https://autoportal.com/autoexpo/').text

    soup = BeautifulSoup(source, 'html.parser')
    for a in soup.find_all('div',{'class':'cell5 cell-md text-center m_b-10'}):
        logo = a.find('img').get('src')
    text=soup.find('p',{'class':'text-md'}).text
    
    return render_template('home.html',logo=logo,text=text)
    




@app.route('/index')
def index():
    data = []
    images=[]
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
        car=['https://cdn.autoportal.com/img/newcars/normal/kia_rio.jpg',
        'https://cdn.autoportal.com/img/newcars/normal/mahindra_thar-facelift.jpg',
        'https://cdn.autoportal.com/img/newcars/normal/mahindra_bolero-facelift-c4c67.jpg',
        'https://cdn.autoportal.com/img/newcars/normal/mahindra_tuv300-facelift-b6521.jpg',
        'https://cdn.autoportal.com/img/newcars/normal/toyota_vios.jpg',
        'https://cdn.autoportal.com/img/newcars/normal/hyundai_xcent-facelift.jpg',
         'https://cdn.autoportal.com/i/catalog/default-cars.png',
         'https://cdn.autoportal.com/img/newcars/normal/volkswagen_t-roc.jpg',
         'https://cdn.autoportal.com/img/newcars/normal/tata_altroz-ev-b316f.jpg',
         'https://cdn.autoportal.com/img/newcars/normal/tata_q502.jpg']
        
            
        
        #for c in soup.find_all('div',{'class':'cell5 cell-sm m_b-20'}):
            #car_info['ov']=c.find('div',{'class':'desc'}).text

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
    
        
    return render_template('index.html',data=data,car=car)






@app.route('/word')
def word():
     
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    text = (''.join(s.findAll(text=True))for s in soup.findAll('p'))

    c = Counter((x.rstrip(punctuation).lower() for y in text for x in y.split()))
    data1 = c.most_common()
    data2=[x for x in c if c.get(x) > 5]
    
    return render_template('word.html',data1=data1,data2=data2)    


@app.route('/contact')
def contact():
    if request.method =="POST":
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            country = request.form['country']
            category = request.form['category']
            contact = request.form['contact']
            create_cus = customer(firstname,lastname,country,category,contact)
            db.session.add(create_cus)
            db.session.commit()
            

    return render_template("contact.html")

        

@app.route('/result',methods = ['POST'])
def result():
    result = request.form
    if request.method =="POST":
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            country = request.form['country']
            category = request.form['category']
            contact = request.form['contact']
            create_cus = customer(firstname,lastname,country,category,contact)
            db.session.add(create_cus)
            db.session.commit()
            res = make_response("<h1>cookie is set</h1>")  
            res.set_cookie('respond',firstname)
    return render_template('result.html', result=result)




@app.route('/about')
def about():
    data=[]
    source = requests.get('https://autoportal.com/aboutus.html').text
    soup = BeautifulSoup(source, 'html.parser')
    source1 = requests.get('https://autoportal.com/feedback.html').text
    soup1 = BeautifulSoup(source1, 'html.parser')
    for b in soup1.find_all('p',{'class':'m_b-10'}):
        con={}
        con['text'] = b.text
        data.append(con)

    for a in soup.find_all('div',{'class':'info-page'}):
        text = a.find('p').text
    
    return render_template('about.html',text=text,data=data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__': 
     app.run(debug=True)
