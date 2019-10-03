import torch
from pytorch_transformers import BertForSequenceClassification, BertTokenizer
from keras.preprocessing.sequence import pad_sequences
from multiprocessing import Pool, cpu_count
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler

MAX_LEN = 50
BATCH_SIZE = 16
tokenizer = BertTokenizer.from_pretrained(
    "bert-base-uncased", do_lower_case=True)


def tokenize(text):
    text = '[CLS] ' + text + ' [SEP]'
    tokens = tokenizer.tokenize(text)
    input_ids = [tokenizer.convert_tokens_to_ids(token) for token in tokens]

    return input_ids


def get_attention_mask(sequence):
    attention_mask = list(map(lambda x: float(x > 0), sequence))
    return attention_mask


def prepare_input(batch):
    with Pool(cpu_count()) as p:
        input_ids = list(p.map(tokenize, batch))

        input_ids = pad_sequences(
            input_ids, maxlen=MAX_LEN,
            dtype="long", truncating="post", padding="post")

        attention_mask = list(p.map(get_attention_mask, input_ids))

    input_ids_list = torch.tensor(input_ids)
    attention_mask_list = torch.tensor(attention_mask)

    data = TensorDataset(input_ids_list, attention_mask_list)
    sampler = SequentialSampler(data)
    dataloader = DataLoader(
        data, sampler=sampler, batch_size=BATCH_SIZE)

    return dataloader


def get_model():
    model = BertForSequenceClassification.from_pretrained(
        "data/model/23919", num_labels=2)
    model.eval()

    return model
