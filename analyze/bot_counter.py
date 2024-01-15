#!/usr/bin/env python3
"""
Usage:
    bot_counter.py [-d DIRECTORY] [-o FILE] [--dname FIELD]

Options:      
    -d DIRECTORY         Input directory [default: resources/results]   
    -o FILE              Output file [default: resources/analyzes/bot_counter.pkl]
"""

import json
import glob
import os

from docopt import docopt
from tqdm import tqdm
import pickle
from p_tqdm import p_map
from helper import is_bot

if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    
    output_tmp_directory = os.path.splitext(output_file)[0]
    os.makedirs(output_tmp_directory, exist_ok=True)


    

    def bot_counter(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            data = json.load(json_file)
            
            count_bot = 0
            
            for commit in data:
                if is_bot(commit):
                    count_bot +=1
                    

            count_non_bot  = len(data) - count_bot
        
                
            with open(project_result_path, "wb") as result_file:
                pickle.dump({"bot": count_bot, "non_bot": count_non_bot}, result_file)

    p_map(bot_counter, input_files)

    print("Done with individual")
    count = {
        "bot": 0,
        "non_bot": 0
    }

    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')

        with open(project_result_path, 'rb') as f:
            results = pickle.load(f)

        count["bot"] += results['bot']
        count["non_bot"] += results['non_bot']

    with open(output_file, 'wb') as fp:
        pickle.dump(count, fp)


    c_b = count['bot']
    c_n_b = count['non_bot']

    print(f'Number of bot commits: {c_b} Percent:{(c_b/c_n_b):.2f} Number of human commits: {c_n_b}')
    




            

