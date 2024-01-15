#!/usr/bin/env python
"""
Usage:
    to_csv_split.py [-h] [-i FILE] [-o FILE]

Options:
    -h --help                           Show this screen.    
    -i FILE                             Input file or folder(if directory is specified) [default: resources/results_big_all_filtered_with_author.csv]
    -o FILE                             Output file or folder(if directory is specified) [default: 'resources/results_big_all_filtered_with_author_deduplicated.csv']
"""

import pandas as pd
from docopt import docopt


if __name__ == '__main__':    
    args = docopt(__doc__)
    
    df = pd.read_csv(args['-i'])


    r = df.groupby('hash')
    l = r.first(0)
    l['hash'] = l.index
    l = l.reset_index(drop=True)
    df = l
    df

    r = df.groupby(['message', 'diff'])

    l = r.first(0)
    l['message'] = l.index.get_level_values(0)
    l['diff'] = l.index.get_level_values(1)

    l = l.reset_index(drop=True)
    df = l

    r = df.groupby('diff')

    l = r.first(0)
    # l['message'] = l.index.get_level_values(0)
    l['diff'] = l.index

    l = l.reset_index(drop=True)
    # df = l
    # df
    df = l

    df.to_csv(args['-o'], index=False)
