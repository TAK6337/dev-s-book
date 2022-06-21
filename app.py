from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.gswdo8n.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
db.devsbook_bestseller.drop()
db.devsbook_front.drop()
db.devsbook_back.drop()


import requests
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?mallGb=KOR&linkClass=33&range=0&kind=1&orderClick=DCb', headers=headers)
bestseller_soup = BeautifulSoup(data.text, 'html.parser')

bestseller_books = bestseller_soup.select('#main_contents > ul > li')

for bestseller_book in bestseller_books:
    booktitle = bestseller_book.select_one('div.detail > div.title > a > strong').text
    price = bestseller_book.select_one('div.price > strong').text
    image = bestseller_book.select_one('div.cover > a > img')
    doc = {
        'booktitle': booktitle,
        'price': price,
        'image': image['src']
    }
    db.devsbook_bestseller.insert_one(doc)

front_data = requests.get('https://search.kyobobook.co.kr/web/search?vPstrKeyWord=react&searchPcondition=1&searchCategory=%EA%B5%AD%EB%82%B4%EB%8F%84%EC%84%9C@KORBOOK@@%EC%BB%B4%ED%93%A8%ED%84%B0/IT@33&collName=KORBOOK&from_CollName=%EC%A0%84%EC%B2%B4@UNION&vPstrTab=PRODUCT&from_coll=KORBOOK&currentPage=1&orderClick=LIZ', headers=headers)
front_soup = BeautifulSoup(front_data.text, 'html.parser')
front_books = front_soup.select('#search_gallery > tr > td')

for front_book in front_books:
    booktitle = front_book.select_one('div > div.title > a > strong').text
    price = front_book.select_one('div > div.price > div.sell_price > strong').text
    image = front_book.select_one('div > div.image > div.cover > a > img')
    doc = {
        'booktitle': booktitle,
        'price': price,
        'image': image['src']
    }
    db.devsbook_front.insert_one(doc)

back_data = requests.get('https://search.kyobobook.co.kr/web/search?vPstrKeyWord=spring&searchPcondition=1&searchCategory=%EA%B5%AD%EB%82%B4%EB%8F%84%EC%84%9C@KORBOOK@@%EC%BB%B4%ED%93%A8%ED%84%B0/IT@33&collName=KORBOOK&from_CollName=%EC%A0%84%EC%B2%B4@UNION&searchOrder=0&vPstrTab=PRODUCT&from_coll=KORBOOK&currentPage=1&orderClick=LIZ', headers=headers)
back_soup = BeautifulSoup(back_data.text, 'html.parser')
back_books = back_soup.select('#search_gallery > tr > td')

for back_book in back_books:
    booktitle = back_book.select_one('div > div.title > a > strong').text
    price = back_book.select_one('div > div.price > div.sell_price > strong').text
    image = back_book.select_one('div > div.image > div.cover > a > img')
    doc = {
        'booktitle': booktitle,
        'price': price,
        'image': image['src']
    }
    db.devsbook_back.insert_one(doc)


@app.route('/', methods=["GET"])
def main_page():
    bestseller_list = list(db.devsbook_bestseller.find({}, {'_id': False}))
    front_list = list(db.devsbook_front.find({}, {'_id': False}))
    back_list = list(db.devsbook_back.find({}, {'_id': False}))
    return render_template('main_page.html',
                           bestseller_list=bestseller_list, front_list=front_list, back_list=back_list
                           )


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

