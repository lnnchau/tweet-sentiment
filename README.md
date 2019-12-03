# A Simple Web API for Tweet Sentiment Analysis

### Introduction
- A simple web API to analyze the overall sentiment towards a topic on Twitter by scraping tweets with the given keyword and predicting their sentiment.
- The inference model is an ensemble of two BERT models, each finetuned on a different dataset. The datasets are SemEval2017 and Sentiment140. The model achieves 87.7% (F1) on Sentiment140's test set.
- To deploy on Heroku's free tie lightweight server, the model is distilled into a Max Entropy classifier with bag-of-word features, which achieves the trade-off F1-score of 82.0% and roughly 2 seconds faster in performance.

### Prepare a clean environment (Python 3.6 is recommended)
```bash
virtualenv env_tweet --python=python3.6
source env_tweet/bin/activate
```

### Start server
The bash script `./local_entrypoint` will help you install necessary packages and download models for inference before starting the server. (`entrypoint.sh` is for deployment on Heroku)
```bash
sudo apt-get wget
chmod +x ./local_entrypoint.sh
./local_entrypoint.sh
```

### Testing
#### Send a request
```bash
curl localhost:5000/analyze/<keyword>
```
#### Response schema
```python
{
  "keyword": str,
  "negative_ratio": float,
  "num_tweets_total": int,
  "positive_ratio": float,
  "processing_time": float,
  "results": [
    {
      "sentiment": enum["POSTITIVE", "NEGATIVE"],
      "text": str,
      "polarity": float,
    },
    {
      "sentiment": enum["POSTITIVE", "NEGATIVE"],
      "text": str,
      "polarity": float,
    },
  ]
}
```
