#!/usr/bin/env python
"""
Usage:
    to_csv_split.py [-h] [-i FILE] [-o FILE]

Options:
    -h --help   Show this screen.    
    -i FILE     Input file or folder(if directory is specified) [default: resources/results_big_all_filtered_with_author.csv]
    -o FILE     Output file or folder(if directory is specified) [default: 'resources/results_big_all_filtered_with_author_bots_removed.csv']
"""

import pandas as pd
from docopt import docopt


if __name__ == '__main__':    
    args = docopt(__doc__)
    
    df = pd.read_csv(args['-i'])

    df = df[~(df['author_email'].str.contains('bot') | df['author_name'].str.contains('bot') | df['comitter_email'].str.contains('bot') | df['comitter_name'].str.contains('bot'))]

    df.to_csv(args['-o'], index=False)
