from os import path
from collections import Counter
import json

datapath = "resources/export/commitgen_big"

def load_split(data_path, split_path, size):
    diff_path = path.join(datapath, f'{split_path}.{size}.diff')
    msg_path = path.join(datapath, f'{split_path}.{size}.msg')

    with open(diff_path, 'r') as f:
        diffs = [l.strip() for l in f.readlines()]

    with open(msg_path, 'r') as f:
        msgs = [l.strip() for l in f.readlines()]
    
    return list(zip (diffs, msgs))

train_data = load_split(datapath, "train", "1085329")


diffs = [d for d,m in train_data]

msgs = [m for d,m in train_data]

diff_vocab_length = 50000
msg_vocab_length = 17000



def generate_vocab(list_of_documents, vocab_length = 50000, special_tokens = ["eos", "UNK"]):
    tokens = [document.split(' ') for document in list_of_documents]
    flat_list = [item for sublist in tokens for item in sublist]
    result = Counter(flat_list)    
    keys = result.most_common(vocab_length - len(special_tokens))
    keys = [k for k, count, in keys]
    keys = special_tokens + keys
    return {key: idx for idx, key in enumerate(keys)}

diff_vocab = generate_vocab(diffs, vocab_length=diff_vocab_length)
msgs_vocab = generate_vocab(msgs, vocab_length=msg_vocab_length)


result_path = path.join(datapath, f'vocab.diff.{diff_vocab_length}.json')
with open(result_path, 'w') as f:
    json.dump(diff_vocab, f)

result_path = path.join(datapath, f'vocab.msg.{msg_vocab_length}.json')
with open(result_path, 'w') as f:
    json.dump(msgs_vocab, f)
