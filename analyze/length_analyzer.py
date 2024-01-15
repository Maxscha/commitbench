#!/usr/bin/env python3
"""
Usage:
    length_analyzer.py [-d DIRECTORY] [-o FILE] [--dname FIELD] [--mname FIELD] [--tokenizer TOKENIZER]

Options:      
    -d DIRECTORY            Input directory [default: resources/results]   
    -o FILE                 Output file [default: resources/analyzes/seq_length_analyzes.pkl] 
    --dname FIELD           Diff Field Name[default: diff]
    --mname FIELD           Message Field name[default: message]
    --tokenizer TOKENIZER   HF-Ttokenizer [default: t5-small]
"""

import json
import glob
import os
from p_tqdm import p_map


from docopt import docopt
import pickle

from transformers import AutoTokenizer
from transformers.utils import logging

from helper import get_sequence_length
# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close

logging.set_verbosity(40)

def process_file(input_file, diff_field_name, message_field_name, tokenizer):
    repo_name = os.path.basename(input_file)

    with open(input_file) as json_file:
        data = json.load(json_file)        

        length_diffs = get_sequence_length(data, tokenizer, diff_field_name)
        length_msg = get_sequence_length(data, tokenizer, message_field_name)
        

    return (repo_name, {"l_diffs": length_diffs, "l_msg": length_msg})

if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')            

    output_file = args['-o']

    diff_field_name = args['--dname']
    message_field_name = args['--mname']

    tokenizer_config = args['--tokenizer']

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_config)
    
    results = {}


    func = lambda x: process_file(x, diff_field_name, message_field_name, tokenizer)

    m_results = p_map(func, input_files, num_cpus=1)
    # m_results = map(func, input_files)
    for project, value in m_results:
        results[project] = value

    
    with open(output_file, 'wb') as fp:
        pickle.dump(results, fp)



            

