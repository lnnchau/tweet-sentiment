import logging
import numpy as np
import torch
import pickle


model = pickle.load(open('data/model/distil.pkl', 'rb'))
logger = logging.getLogger(__name__)
mappings = {
    0: "NEGATIVE",
    1: "POSITIVE"
}


def inference_batch(batch):
    logits = model.predict(batch)
    res = np.argmax(logits, axis=1)

    for tweet, label, l in list(zip(batch, res, logits)):
        logger.debug(f'\nL: {l}\nLabel: {label}\n{tweet}')

    labels = [mappings[r] for r in res]
    return labels, res

