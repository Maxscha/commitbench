#!/usr/bin/env python
"""
Usage:
    csv_split_to_commitgen.py [-h] [-i FILE] [-o DIRECTORY] [-m INT] [-d INT]

Options:
    -h --help                       Show this screen.
    -i FILE                         Input file or folder(if directory is specified) [default: resources/results.csv]
    -o DIRECTORY                    Output file or folder(if directory is specified) [default: resources/export/results_commitgen]
    -m INT                          Maximum number if message vocabulary [default: 1000]
    -d INT                          Maximum number of days per file [default: 365]
"""


import json
import os
import pandas as pd
import shutil
from docopt import docopt

from collections import Counter

if __name__ == '__main__':    
    args = docopt(__doc__)

    def get_vocab(series):
        r = series.apply(lambda x: set([l.strip() for l in x.split(' ')]))
        c = Counter([l for s in r for l in s])
        return c

    def filter_vocab(counter:Counter, threshold:int = 10, max_elements = None):
        filtered =  Counter(el for el in counter.elements() if counter[el] >= threshold)
        return list([key for key, value in filtered.most_common(max_elements)])


    def convert_vocab_json(vocab):
        dic = {
            "eos": 0,
            "UNK": 1,
            "<n>": 2
        }

        for idx, vocab in enumerate(vocab):
            dic[vocab] = idx + 3

        dic["eos"] = 0

        return dic



    input_csv = args['-i']

    output_folder = args['-o']

    shutil.rmtree(output_folder, ignore_errors=True)

    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(input_csv)
    splits = ["train", "valid", "test"]

    df.message = df.message.apply(lambda x: str(x))

    df.loc[(df["split"] == 'val'), 'split'] = 'valid'
    # VOCAB

    source_vocab = get_vocab(df[(df["split"] == 'train')]["diff"])
    target_vocab = get_vocab(df[(df["split"] == 'train')]["message"])

    source_vocab = filter_vocab(source_vocab, threshold=10)
    target_vocab = filter_vocab(target_vocab, threshold=10)

    len_split = {
        "train": df[(df["split"] == 'train')].shape[0],
        "valid": df[(df["split"] == 'valid')].shape[0],
        "test": df[(df["split"] == 'test')].shape[0]
    }


    print(len_split)
    for idx, row in df.iterrows():
        msg = row["message"]
        diff = row["diff"].replace('\n', '<n>')
        split = row["split"].replace('\n', '<n>')
        with open(os.path.join(output_folder, f'{split}.{len_split[split]}.diff'), "a+") as f:
            f.write(diff + "\n")

        with open(os.path.join(output_folder, f'{split}.{len_split[split]}.msg'), "a+") as f:
            f.write(msg.replace('\n', '') + "\n")


    with open(os.path.join(output_folder, f'vocab.diff.{len(source_vocab) + 3}.json'), "w") as f:
        json.dump(convert_vocab_json(source_vocab), f)

    with open(os.path.join(output_folder, f'vocab.msg.{len(target_vocab) + 3}.json'), "w") as f:
        json.dump(convert_vocab_json(target_vocab), f)

