import logging
import pickle
import numpy as np
from scipy.special import expit as sigmoid


model = pickle.load(open('data/model/distil.pkl', 'rb'))
logger = logging.getLogger(__name__)
mappings = {
    0: "NEGATIVE",
    1: "POSITIVE"
}


def inference_batch(batch):
    logits = model.predict(batch)
    res = np.argmax(logits, axis=1)

    probs = sigmoid(logits)
    polarity = probs[:, 1] - probs[:, 0]

    for tweet, label, l, p in list(zip(batch, res, logits, polarity)):
        logger.debug(f'\nL: {l}\nLabel: {label}\n{tweet}\nPolarity: {p}')

    labels = [mappings[r] for r in res]
    return labels, res, polarity
