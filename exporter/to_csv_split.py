#!/usr/bin/env python
"""
Usage:
    to_csv_split.py [-h] [-t] [-i DIRECTORY] [-o FILE] [--keep_duplicates] [-s SEED] [--keep_authors] [--use_existing_split FILE]

Options:
    -h --help                           Show this screen.    
    -t                                  Tiny
    -i DIRECTORY                        Input file or folder(if directory is specified) [default: resources/filtered]
    -o FILE                             Output file or folder(if directory is specified) [default: 'resources/results_big_all_filtered.csv']
    --keep_duplicates                   Keep duplicates
    --s                                 Seed for random number generator [default: 42]
    --keep_authors                      Keep authors in the dataset [default: False]
    --use_existing_split FILE           Use existing split file to split the data [default: None]
"""


# Load files

from docopt import docopt
import glob
import json
import os
import pandas as pd
from tqdm import tqdm


if __name__ == '__main__':    
    args = docopt(__doc__)

    existing_results = glob.glob(args['-i'] + '/*.json')

    print(f'Found {len(existing_results)} files')
    tiny = args['-t']
    keep_duplicates = args['--keep_duplicates']
    drop_authors = not args['--keep_authors']
    seed = int(args['-s'])

    train = 0.7
    test = 0.15
    val = 0.15

    if tiny:
        train = 0.33
        test = 0.33
        val = 0.33

    all_commits = []
    for result in tqdm(existing_results):
        base=os.path.basename(result)
        org_project = os.path.splitext(base)[0]
        with open(result) as f:                       
            loaded = json.load(f)
            for l in loaded:
                for k in l.keys():
                    # Need to replace \r with \n otherwise the csv will be broken
                    l[k] = l[k].replace('\r', '\n')
                l['project'] = org_project
            all_commits.extend(loaded)

    # random.shuffle(all_commits)



    if tiny:
        all_commits = all_commits[:30]

    df = pd.DataFrame(all_commits)
    
    if args['--use_existing_split'] is not None:
        print(f'Using existing split file {args["--use_existing_split"]}')
        df_existing = pd.read_csv(args['--use_existing_split'])
        assert len(set(df_existing['hash']) - set(df['hash'])) == 0, "Not all commits are in the new dataset, maybe sth. was deleted or the preprocessing went wrong"
        
        df = df_existing[['hash', 'split', 'project']].join(df.set_index(['hash', 'project']), on=['hash', 'project'], how='inner')
        
    else:
        print("Generate new split")
    
        if not keep_duplicates:
            df = df.drop_duplicates(subset=['message', 'diff'])
        
        if drop_authors:
            df = df.drop(columns=['author_email', 'author_name', 'committer_email', 'committer_name'])
        
        df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

        length_df = len(df)

        def get_split(index):
            percent = int(index) / length_df
            if percent < train:
                return 'train'
            elif percent < train + val:
                return 'val'
            else:
                return 'test'

        df['split'] = df.apply(lambda x: get_split(x.name), axis=1)

    


    output_path = args['-o']

    if tiny:
        path = output_path + '_tiny'
    else:
        path = output_path
    df.to_csv(path, index=False)

    print(f'Wrote {len(df)} rows to {path}')
