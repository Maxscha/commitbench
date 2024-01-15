#!/usr/bin/env python3
"""
Usage:
    drop_fields.py [-h] [-i FILE] [-o FILE] [-c COLUMNS]


Options:
    -h --help                           Show this screen.
    -i FILE                             Input file or folder(if directory is specified) [default: resources/results_enhanced.csv]
    -o FILE                             Output file or folder(if directory is specified) [default: resources/results_finished.csv]
    -c COLUMNS                          Columns to drop, separated by a comma [default: author_email,author_name,committer_email,committer_name]
"""

from docopt import docopt
import pandas as pd

def main():
    args = docopt(__doc__)
    
    input_path = args["-i"]
    output_path = args["-o"]

    columns = args["-c"].split(",")

    df = pd.read_csv(input_path)

    print(f'Existing columns {df.columns}')
    print(f'Dropping columns {columns}')
    
    df.drop(columns, inplace=True, axis=1)    

    print(f'Remaining columns {df.columns}')

    df.to_csv(output_path, index=False)



if __name__ == '__main__':
    main()
