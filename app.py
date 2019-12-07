from flask import Flask, request
from procedure.preprocess import clean_tweet
from procedure.predict import inference_batch
from procedure.scrape import get_tweet
from multiprocessing import Pool, cpu_count
import logging
import json
import time

logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(filename='logs/app.log')],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():

    return "Type /analyze/<kw> to start"


@app.route('/analyze/<name>', methods=['GET'])
def analyze(name):
    start = time.time()

    app.logger.info(f'Keyword: {name}')
    tweets = get_tweet(name)
    app.logger.info(f'Scraped {len(tweets)} tweets')

    with Pool(cpu_count()) as p:
        input_text = list(p.imap(clean_tweet, tweets))

    labels, res, polarity = inference_batch(input_text)

    res_dict = {
        "keyword": name,
        "num_tweets_total": len(tweets),
        "positive_ratio": sum(res) / max(len(tweets), 1),
        "results": [{
            "text": text,
            "sentiment": label,
            "polarity": p
        } for text, label, p in list(zip(tweets, labels, polarity))]
    }
    res_dict["negative_ratio"] = 1 - res_dict["positive_ratio"]
    res_dict["processing_time"] = time.time() - start

    return res_dict
