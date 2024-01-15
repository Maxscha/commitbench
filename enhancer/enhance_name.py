#!/usr/bin/env python3
"""
It is a seperate file, cause this operation is rather slow and the operation can deadlock.
Usage:
    enhance_name.py [-h] [-i FILE] [-o FILE]


Options:
    -h --help                           Show this screen.
    -i FILE                             Input file or folder(if directory is specified) [default: resources/results.csv]
    -o FILE                             Output file or folder(if directory is specified) [default: resources/results_enhanced.csv]
"""

from docopt import docopt
import pandas as pd
from helper import replace_name
from tqdm import tqdm
import swifter

tqdm.pandas()

def main():
    args = docopt(__doc__)
    
    input_path = args["-i"]
    output_path = args["-o"]

    df = pd.read_csv(input_path)
    
    df['message_cleaned'] = df['message'].swifter.apply(replace_name)

    df.to_csv(output_path, index=False)



if __name__ == '__main__':
    main()
