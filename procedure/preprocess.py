from bs4 import BeautifulSoup
from pathlib import Path
import re
import json
import logging

logger = logging.getLogger(__name__)

mention_pattern = r'@[A-Za-z0-9]+'
link_pattern = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((mention_pattern, link_pattern))
abbr_dict = json.load(Path(Path(__file__).parent / 'abbr_dict.json').open())


def clean_tweet(text):
    html_decoded = BeautifulSoup(text, 'lxml').get_text().lower()
    clean_mention_link = re.sub(combined_pat, '', html_decoded)

    try:
        clean_utf = clean_mention_link.decode(
            "utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean_utf = clean_mention_link

    norm_abbr = clean_utf
    for abbr in abbr_dict.keys():
        norm_abbr = norm_abbr.replace(abbr, abbr_dict[abbr])

    clean_punc = re.sub("[^a-zA-Z|\n]", " ", norm_abbr)
    clean_space = re.sub("[\s]+", " ", clean_punc)
    clean_tweet = clean_space.strip()

    logger.info(f'Raw: {text}\nCleaned: {clean_tweet}')

    return clean_tweet
