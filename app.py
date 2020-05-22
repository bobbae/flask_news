from flask import (Flask,render_template,request,Response,jsonify)
from newscatcher import Newscatcher
from newscatcher import urls, describe_url
import logging
from logging.handlers import RotatingFileHandler
import re

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
handler = RotatingFileHandler('flask_news.log',maxBytes=10000,backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.info('starting')

@app.route('/')
def myindex():
    global lacovidlist
    app.logger.info("myindex")
    return render_template("index.html",news=get_news('latimes.com'), next_page=1, prev_page=0)

topics = [ 'tech', 'news', 'business', 'science', 'finance', 
        'food', 'politics', 'economics', 'travel', 'entertainment', 
        'music', 'sport', 'world' ]

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_news(sitename):
    nc = Newscatcher(website = sitename)
    results = nc.get_news()
    articles = results['articles']
    #nytimes.print_headlines(n=10)
    #urls_pol = urls(topic = 'politics')
    #describe_url(urls_pol[1])
    #atlantic = Newscatcher(website = urls_pol[1], topic = 'politics')    
    for a in articles:
        a.source = sitename
        a.summary = cleanhtml(a.summary)
    return articles

if __name__=='__main__':
    app.run(threaded=True, port=5000)
