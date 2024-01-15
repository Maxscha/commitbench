#!/usr/bin/env python3
"""
Usage:
    reverte_counter.py [-d DIRECTORY] [-o FILE] [--mname FIELD]

Options:      
    -d DIRECTORY         Input directory [default: resources/results_dobj]   
    -o FILE              Output file [default: resources/analyzes/reverte_counter.pkl] 
    --mname FIELD        Message Field Name [default: message]
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
from helper import is_revert

# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close


if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    

    output_tmp_directory = os.path.splitext(output_file)[0]
    
    os.makedirs(output_tmp_directory, exist_ok=True)


    message_field_name = args['--mname']
    print(message_field_name)

    def revert_counter(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            data = json.load(json_file)
            
            count_revert = 0
            count_non_revert = 0
            for commit in data:
                if is_revert(commit, message_field_name):
                    count_revert +=1
                else:
                    count_non_revert +=1
                    
                
            with open(project_result_path, "wb") as result_file:
                pickle.dump({"revert": count_revert, "non_revert": count_non_revert}, result_file)

    p_map(revert_counter, input_files)

    print("Done with individual")
    count = {
        "revert": 0,
        "non_revert": 0
        
    }

    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')

        with open(project_result_path, 'rb') as f:
            results = pickle.load(f)

        count["revert"] += results['revert']
        count["non_revert"] += results['non_revert']

    with open(output_file, 'wb') as fp:
        pickle.dump(count, fp)


    c_b = count['revert']
    c_n_b = count['non_revert']

    print(f'Number of revert: {c_b} Number of non revert: {c_n_b}')





            

