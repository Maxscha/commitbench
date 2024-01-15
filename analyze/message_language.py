#!/usr/bin/env python3
"""
Usage:
    message_language.py [-d DIRECTORY] [-o FILE] [--mname FIELD]

Options:      
    -d DIRECTORY         Input directory [default: resources/results]   
    -o FILE              Output file [default: resources/analyzes/message_language.pkl]     
    --mname FIELD        Message Field name[default: message]    
"""

import json
import glob
import os

from docopt import docopt
from tqdm import tqdm
import pickle
from collections import Counter
from p_tqdm import p_map


from helper import get_message_language

if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    

    output_tmp_directory = os.path.splitext(output_file)[0]
    
    os.makedirs(output_tmp_directory, exist_ok=True)


    message_field_name = args['--mname']

    def message_language(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            data = json.load(json_file)
            
            languages = []
            
            for commit in data:
                languages.append(get_message_language(commit, message_field_name))

            with open(project_result_path, "wb") as result_file:
                pickle.dump(languages, result_file)

    p_map(message_language, input_files)

    print("Done with individual")
    languages = []

    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')

        with open(project_result_path, 'rb') as f:
            language = pickle.load(f)

        languages.extend(language)

    with open(output_file, 'wb') as fp:
        pickle.dump(languages, fp)
    
