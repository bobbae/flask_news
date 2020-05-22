from flask import (Flask,render_template,request,Response,jsonify)
from newscatcher import Newscatcher
from newscatcher import urls, describe_url
import logging
from logging.handlers import RotatingFileHandler
import re
import pdb

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
handler = RotatingFileHandler('flask_news.log',maxBytes=10000,backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.info('starting')

topics = [ 'tech', 'news', 'business', 'science', 'finance', 
        'food', 'politics', 'economics', 'travel', 'entertainment', 
        'music', 'sport', 'world' ]

sites = [ 'latimes.com', 'reuters.com',  'nytimes.com', 'theatlantic.com', 
            'yahoo.com', 'bbc.co.uk', 'ft.com', 'pbs.org', 'nbcnews.com',
          'washingtonpost.com', 'independent.co.uk', 'cnbc.com', 'cnn.com',
          'newyorker.com', 'nypost.com', 'qz.com', 'dw.com', 'rt.com',
          'nymag.com', 'vox.com', 'theglobeandmail.com', 'express.co.uk',
          'salon.com', 'vanityfair.com', 'standard.co.uk', 'chicagotribune.com'
        ]

@app.route('/')
def myindex():
    app.logger.info("myindex")
    page = request.args.get('page', 1)
    source = request.args.get('source', '')

    try: 
        page = int(page)
    except:
        page = 1

    if page < 1:
        page = 1

    if len(sites) < page:
        app.logger.info("page %d out of range", page)
        return render_template('index.html',news=[], next_page= 1)

    if source != '':
        if not source in sites:
            return render_template('index.html',news=[], next_page= 1)
    else:
        source = sites[page - 1]

    return render_template('index.html',news=get_news(source), next_page=page + 1)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_news(source):
    nc = Newscatcher(website = source)
    results = nc.get_news()
    articles = results['articles']
    app.logger.info("len articles %d", len(articles))
    i= 0
    retval = []
    for a in articles:
        # skip articles without summary
        if 'summary' in a.keys():
            b = a
            a.source = source
            a.summary = cleanhtml(a.summary)
            retval.append(b)
    return retval

def describe_sources(source):
    nc = Newscatcher(website = source)
    nc.print_headlines(n=10)
    urls_pol = urls(topic = 'politics')
    describe_url(urls_pol[1])
    res = Newscatcher(website = urls_pol[1], topic = 'politics')    

if __name__=='__main__':
    app.run(threaded=True, port=5000)
