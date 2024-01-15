#!/usr/bin/env python
"""
Usage:
    split_csv.py [-h] [-i FILE] [-o DIRECTORY]

Options:
    -h --help                       Show this screen.
    -i FILE                         Input file [default: resources/results.csv]
    -o DIRECTORY                    Output folder, the default is resources/filename/
"""

import os
import pandas as pd
import shutil
from docopt import docopt
from pathlib import Path

if __name__ == '__main__':    
    args = docopt(__doc__)

    input_csv = args['-i']

    stem = Path(input_csv).stem

    output_folder = args['-o']

    if not output_folder:
        output_folder = f'resources/{stem}'


    shutil.rmtree(output_folder, ignore_errors=True)

    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(input_csv)

    splits = ["train", "val", "test"]

    len_split = {
        "train": df[(df["split"] == 'train')].shape[0],
        "valid": df[(df["split"] == 'valid')].shape[0],
        "test": df[(df["split"] == 'test')].shape[0]
    }

    for split in splits:
        df_split = df[(df["split"] == split)]
        df_split.to_csv(os.path.join(output_folder, split + ".csv"), index=False)

