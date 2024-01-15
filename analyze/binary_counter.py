#!/usr/bin/env python3
"""
Usage:
    binary_counter.py [-d DIRECTORY] [-o FILE] [--dname FIELD]

Options:      
    -d DIRECTORY         Input directory [default: resources/results]   
    -o FILE              Output file [default: resources/analyzes/binary_counter.pkl] 
    --dname FIELD        Diff Field Name[default: diff]    
"""

import json
import glob
import os

from docopt import docopt
from tqdm import tqdm
import pickle
from p_tqdm import p_map
from helper import is_binary


if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    

    output_tmp_directory = os.path.splitext(output_file)[0]
    
    os.makedirs(output_tmp_directory, exist_ok=True)


    diff_field_name = args['--dname']

    def binary_counter(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            data = json.load(json_file)
            
            count_binary = 0
            count_non_binary = 0
            
            for commit in data:
                if is_binary(commit, field = diff_field_name):
                    count_binary +=1
                else:
                    count_non_binary +=1
                    
                
            with open(project_result_path, "wb") as result_file:
                pickle.dump({"binary": count_binary, "non_binary": count_non_binary}, result_file)

    p_map(binary_counter, input_files)

    print("Done with individual")
    count = {
        "binary": 0,
        "non_binary": 0
    }

    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')

        with open(project_result_path, 'rb') as f:
            results = pickle.load(f)

        count["binary"] += results['binary']
        count["non_binary"] += results['non_binary']

    with open(output_file, 'wb') as fp:
        pickle.dump(count, fp)


    c_b = count['binary']
    c_n_b = count['non_binary']

    print(f'Number of binary: {c_b} Number of non binary: {c_n_b}')
    # I need java, py, rb, php, go, js




            

