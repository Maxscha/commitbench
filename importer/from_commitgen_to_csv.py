#!/usr/bin/env python
"""
Usage:
    from_commitgen_to_csv.py [-h] [-i DIRECTORY] [-o FILE] [--train FILE] [--test FILE] [--valid FILE]

Options:
    -h --help       Show this screen.    
    -i DIRECTORY    Input folder [default: resources/commitgen]
    -o FILE         Output file [default: resources/commitgen.csv]
    --train FILE    Train File Name [default: train.26208]
    --valid FILE    Valid File Name [default: valid.3000]
    --test FILE     Test File Name [default: test.3000]
"""

from os import path
import pandas as pd
from docopt import docopt


if __name__ == '__main__':    
    args = docopt(__doc__)

    datapath = args['-i']
    train = args['--train']
    valid = args['--valid']
    test = args['--test']
    output_path = args['-o']


    def load_split(datapath, split_path, split_name):
        diff_path = path.join(datapath, f'{split_path}.diff')
        msg_path = path.join(datapath, f'{split_path}.msg')

        with open(diff_path, 'r') as f:
            diffs = [l.strip() for l in f.readlines()]

        with open(msg_path, 'r') as f:
            msgs = [l.strip() for l in f.readlines()]
        
        data = []
        for diff , msg in zip (diffs, msgs) :
            data.append({
                "message": msg,
                "diff": diff,
                "split": split_name
            })
        return data

    train_data = load_split(datapath, train, "train")
    val_data = load_split(datapath, valid, "val")
    test_data = load_split(datapath, test, "test")


    train_data.extend(val_data)
    train_data.extend(test_data)

    data = train_data

    print(len(data))
    df = pd.DataFrame(data)

    df.to_csv(output_path, index=False)
