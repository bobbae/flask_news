from flask import (Flask,render_template,request,Response,jsonify,redirect,url_for)
import random
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

sites = urls(language='EN')

HN = 'https://hacker-news.firebaseio.com/v0'

@app.route('/')
def myindex():
    app.logger.info("myindex")
    return redirect(url_for('do_hn'))

@app.route('/hn')
def do_hn():
    app.logger.info("do_hn")
    page,limit = getparams()
    return render_template('hn_index.html',news=get_hn(page,limit), next_page=page + 1)

def getparams():
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 20)
    page = checkparam(page,1)
    limit = checkparam(limit,20)
    return page,limit

@app.route('/source/<source>')
def do_source(source):
    app.logger.info("do_source")
    page,limit = getparams()
    if source == 'random':
        source = random.choice(sites)
    if not source in sites:
        return render_template('index.html',news=[], next_page= 1, 
                    message='Invalid data source {}'.format(source))
    return render_template('index.html',news=get_news(source,page,limit), next_page=page + 1)
    
@app.route('/sources')
def list_sources():
    return render_template('index.html',news=[], next_page=1,
            message='Available sources are: {} '.format(sites))

def checkparam(p,default):
    try:
        n = int(p)
    except:
        n = default
    if n < default:
        n = default
    return n

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_news(source,page,limit):
    nc = Newscatcher(website = source)
    results = nc.get_news()
    articles = results['articles']
    app.logger.info("len articles %d", len(articles))
    i= 0
    retval = []
    offset = limit *( page - 1)
    for a in articles[offset:limit+offset]:
        # skip articles without summary
        if 'summary' in a.keys():
            b = a
            a.source = source
            a.summary = cleanhtml(a.summary)
            retval.append(b)
    return retval

def get_hn(page, limit):
    responses = loop.run_until_complete(get_topics(page, limit))
    news = []

    for r in responses:
        #n = requests.get(HN+'/item/{}.json'.format(r))
        #nj = n.json()
        nj = r.json()
        unixTime = float(nj['time'])
        utc_time = datetime.utcfromtimestamp(unixTime)
        nj['time'] = utc_time.strftime("%Y-%m-%d %H:%M:%S (UTC)")
        news.append(nj)
    return news

async def get_topics(page, limit):
    res = requests.get(HN+'/topstories.json')
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
            for t in topstories[offset:limit+offset]
        ]
        for response in await asyncio.gather(*futures):
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

