from flask import (Flask,render_template,request,Response,jsonify)
from newscatcher import Newscatcher
from newscatcher import urls, describe_url
import logging
from logging.handlers import RotatingFileHandler
import re
import pdb
import requests
from datetime import datetime
import concurrent.futures
import asyncio

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
handler = RotatingFileHandler('flask_news.log',maxBytes=10000,backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.info('starting')
loop = asyncio.get_event_loop()

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

HN = 'https://hacker-news.firebaseio.com/v0'

@app.route('/')
def myindex():
    app.logger.info("myindex")
    page = request.args.get('page', 1)
    source = request.args.get('source', '')
    limit = request.args.get('limit', 20)

    try: 
        page = int(page)
    except:
        page = 1
    if page < 1:
        page = 1

    try: 
        limit = int(limit)
    except:
        limit = 20
    if limit < 1:
        limit = 20

    if source == "hn":
        return render_template('hn_index.html',news=get_hn(), next_page=page + 1)

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

def get_hn():
    responses = loop.run_until_complete(get_topics())
    #for r in res.json()[offset:]:
    news = []
    print("responses {}".format(responses))

    for r in responses:
        #n = requests.get(HN+'/item/{}.json'.format(r))
        #nj = n.json()
        nj = r.json()
        unixTime = float(nj['time'])
        utc_time = datetime.utcfromtimestamp(unixTime)
        nj['time'] = utc_time.strftime("%Y-%m-%d %H:%M:%S (UTC)")
        news.append(nj)
    return news

async def get_topics():
    res = requests.get(HN+'/topstories.json')
    limit = 20
    page = 1
    offset = limit *( page - 1)
    topstories = res.json()
    responses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=limit) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(t)
            )
            for t in topstories[:limit]
        ]
        for response in await asyncio.gather(*futures):
            print("append {}".format(response))
            responses.append(response)
    return responses

def describe_sources(source):
    nc = Newscatcher(website = source)
    nc.print_headlines(n=10)
    urls_pol = urls(topic = 'politics')
    describe_url(urls_pol[1])
    res = Newscatcher(website = urls_pol[1], topic = 'politics')    

if __name__=='__main__':
    #asyncio.set_event_loop(asyncio.new_event_loop())
    app.run(threaded=True, port=5000)
