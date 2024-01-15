#!/usr/bin/env python3
"""
Usage:
    commit_count.py [-d DIRECTORY] [-o FILE]

Options:      
    -d DIRECTORY         Input directory [default: resources/result]    
    -o FILE              Output file [default: resources/analyzes/commit_count.pkl]
"""

import json
import glob
import os
import pickle

from docopt import docopt
from tqdm import tqdm
from p_tqdm import p_map


# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close

def count_commits(input_file):
    repo_name = os.path.basename(input_file)
    

    with open(input_file) as json_file:
        data = json.load(json_file)
        number_of_commits = len(data)
        return (repo_name, number_of_commits)
        
if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')            

    output_file = args["-o"]

    results = {}

    if os.path.isfile(output_file):
        with open(output_file, 'rb') as fp:
            results = pickle.load(fp)
    else:
        m_results = p_map(count_commits, input_files)
        for project, value in m_results:
            results[project] = value
        with open(output_file, 'wb') as fp:
            pickle.dump(results, fp)

    number_of_repos = len(results.keys())
    number_of_commits = sum(results.values())
    print(f'Number of Repositories: {number_of_repos} Number of Commits: {number_of_commits}')

    


            

