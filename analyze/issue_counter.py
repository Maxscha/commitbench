#!/usr/bin/env python3
"""
Usage:
    issue_counter.py [-d DIRECTORY] [-o FILE] [--dname FIELD]

Options:      
    -d DIRECTORY            Input directory [default: resources/results]   
    -o FILE                 Output file [default: resources/analyzes/issue_counter.pkl]
    --dname FIELD           Field to analzye [default: message]
"""

import json
import glob
import os

from docopt import docopt
from tqdm import tqdm
import pickle
from collections import Counter
from p_tqdm import p_map
import re

# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close


if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    
    output_tmp_directory = os.path.splitext(output_file)[0]

    field = args['--dname']
    os.makedirs(output_tmp_directory, exist_ok=True)


    

    def issue_counter(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            repository = json.load(json_file)        
        
        results = []
        issue_regex = r'#[0-9]+'

        for commit in repository:
            issue_matches = re.findall(issue_regex, commit[field])
            num_issues = len(issue_matches)
            results.append(num_issues)
            
        with open(project_result_path, "wb") as result_file:
            pickle.dump(results, result_file)

    p_map(issue_counter, input_files)
    # res = list(map(issue_counter, input_files))

    print("Done with individual")

    issues = []
    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')

        with open(project_result_path, 'rb') as f:
            issues.extend(pickle.load(f))



    with open(output_file, 'wb') as fp:
        pickle.dump(issues, fp)


    # print(sum(lines)/len(lines))
    
    




            

