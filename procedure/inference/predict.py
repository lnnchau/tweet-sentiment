import logging
from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from keras.preprocessing.sequence import pad_sequences
from pytorch_transformers import BertForSequenceClassification, BertTokenizer

model = BertForSequenceClassification.from_pretrained(
    "data/model/23919", num_labels=2)
model.eval()

tokenizer = BertTokenizer.from_pretrained(
    "bert-base-uncased", do_lower_case=True)


logger = logging.getLogger(__name__)
mappings = {
    0: "NEGATIVE",
    1: "POSITIVE"
}
MAX_LEN = 50


def tokenize(text):
    text = '[CLS] ' + text + ' [SEP]'
    tokens = tokenizer.tokenize(text)
    input_ids = [tokenizer.convert_tokens_to_ids(token) for token in tokens]

    return input_ids


def get_attention_mask(sequence):
    attention_mask = list(map(lambda x: float(x > 0), sequence))
    return attention_mask


def inference_batch(batch):
    with Pool(cpu_count()) as p:
        input_ids = list(p.map(tokenize, batch))

        input_ids = pad_sequences(
            input_ids, maxlen=MAX_LEN,
            dtype="long", truncating="post", padding="post")

        attention_mask = list(p.map(get_attention_mask, input_ids))

    input_ids_list = torch.tensor(input_ids)
    attention_mask_list = torch.tensor(attention_mask)

    batch_size = 16
    pr_data = TensorDataset(input_ids_list, attention_mask_list)
    pr_sampler = SequentialSampler(pr_data)
    pr_dataloader = DataLoader(
        pr_data, sampler=pr_sampler, batch_size=batch_size)

    res = []

    for ids, mask in pr_dataloader:
        with torch.no_grad():
            logits = model(ids, token_type_ids=None,
                           attention_mask=mask)[0].detach().numpy()

        res.extend(np.argmax(logits, axis=1).flatten())

        for tweet, label, l1, l2 in list(zip(batch, res, logits.tolist()):
            logger.debug(f'\nL1: {l1}\nL2: {l2}\nLabel: {label}\n{tweet}')

    labels = [mappings[r] for r in res]
    return labels, res

