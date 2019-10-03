# tweet-sentiment

### Prepare a clean environment (Python 3.6 is recommended)
```bash
virtualenv env_tweet --python=python3.6
source env_tweet/bin/activate
```

### Start server
The bash script `./entrypoint` will help you install necessary packages and download models for inference before starting the server. Take a 5-minute coffee break!
```bash
sudo apt-get wget
chmod +x ./entrypoint
./entrypoint
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
  "processing_time: float,
  "results": [
    {
      "sentiment": enum["POSTITIVE", "NEGATIVE"],
      "text": str
    },
    {
      "sentiment": enum["POSTITIVE", "NEGATIVE"],
      "text": str
    },
  ]
}
```
