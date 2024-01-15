#!/usr/bin/env python3
"""
Usage:
    token_analyzer.py [-d DIRECTORY] [-o FILE] [--dname FIELD] [--mname FIELD] [--tokenizer TOKENIZER]

Options:      
    -d DIRECTORY            Input directory [default: resources/results]   
    -o FILE                 Output file [default: resources/analyzes/token_analyzes.pkl] 
    --dname FIELD           Diff Field Name[default: diff]
    --mname FIELD           Message Field name[default: message]
    --tokenizer TOKENIZER   HF-Ttokenizer [default: t5-small]
"""

import json
import glob
import os

from docopt import docopt
from tqdm import tqdm
import pickle
from collections import Counter
from p_tqdm import p_map

from transformers import AutoTokenizer
# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close

from transformers.utils import logging

# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close

logging.set_verbosity(40)

if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    

    output_tmp_directory = os.path.splitext(output_file)[0]
    
    os.makedirs(output_tmp_directory, exist_ok=True)


    diff_field_name = args['--dname']
    message_field_name = args['--mname']

    tokenizer = AutoTokenizer.from_pretrained(args['--tokenizer'])


    def count_tokens(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        # print(repo_name)
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            data = json.load(json_file)
            
            diff_token_counter = Counter()
            msg_token_counter = Counter()

            #Counter
            diffs= [d[diff_field_name] for d in data]
            if len(diffs) > 0:
                diffs = tokenizer(diffs)
            for d in diffs:
                diff_token_counter.update(d)

            msgs = [d[message_field_name] for d in data]
            if len(msgs) > 0:
                msgs = tokenizer(msgs)

            for m in msgs:
                msg_token_counter.update(m)

            # number_of_commits = len(data)
            # results[repo_name] = {"l_diffs": length_diffs, "l_msg": length_msg}
            with open(project_result_path, "wb") as result_file:
                pickle.dump({"diff": diff_token_counter, "msg": msg_token_counter}, result_file)

    p_map(count_tokens, input_files)

    print("Done with individual")
    diff_token_counter = Counter()
    msg_token_counter = Counter()

    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')

        with open(project_result_path, 'rb') as f:
            result = pickle.load(f)
        diff_token_counter.update(result['diff'])
        msg_token_counter.update(result['msg'])

    with open(output_file, 'wb') as fp:
        pickle.dump({"diff": diff_token_counter, "msg": msg_token_counter}, fp)



            

