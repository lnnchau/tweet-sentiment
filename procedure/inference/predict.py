import logging
import numpy as np
import torch
from .utils import prepare_input, get_model


model = get_model()
logger = logging.getLogger(__name__)
mappings = {
    0: "NEGATIVE",
    1: "POSITIVE"
}


def inference_batch(batch):
    dataloader = prepare_input(batch)
    res = []

    for ids, mask in dataloader:
        with torch.no_grad():
            logits = model(ids, token_type_ids=None,
                           attention_mask=mask)[0].detach().numpy()

        res.extend(np.argmax(logits, axis=1).flatten())

        for tweet, label, l in list(zip(batch, res, logits.tolist())):
            logger.debug(f'\nL: {l}\nLabel: {label}\n{tweet}')

    labels = [mappings[r] for r in res]
    return labels, res
