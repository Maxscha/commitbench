#!/usr/bin/env python3
"""
It is a seperate file, cause this operation is rather slow and the operation can deadlock.
Usage:
    enhance_language.py [-h] [-i FILE] [-o FILE]


Options:
    -h --help                           Show this screen.
    -i FILE                             Input file or folder(if directory is specified) [default: resources/results.csv]
    -o FILE                             Output file or folder(if directory is specified) [default: resources/results_enhanced.csv]
"""

from docopt import docopt
import pandas as pd
from helper import replace_name
from tqdm import tqdm
import re

tqdm.pandas()

def line_to_extension(line):
    file = [item for item in line.split(' ') if item.strip() != '']
    # take until first /
    res = []
    for item in reversed(file):
        if item != '/':
            res.append(item)
        else:
            break
    res = list(reversed(res))
    file = ''.join(res)
    
    if '.' in file:
        return file.split('.')[-1]
    else:
        return file.split('/')[-1]

def get_diff_languages(commit, field='diff'):
    pattern = '^diff --git a/.*'
    diff = commit[field]
    
    files_changed = re.findall(pattern, diff, re.MULTILINE)
    extensions = [line_to_extension(line) for line in files_changed]

    return ','.join(extensions)

def main():
    args = docopt(__doc__)
    
    input_path = args["-i"]
    output_path = args["-o"]

    df = pd.read_csv(input_path)
    
    df['diff_languages'] = df.progress_apply(lambda row: get_diff_languages(row), axis=1)

    df.to_csv(output_path, index=False)



if __name__ == '__main__':
    main()
