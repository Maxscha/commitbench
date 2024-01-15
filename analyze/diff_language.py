#!/usr/bin/env python3
"""
Usage:
    diff_language.py [-d DIRECTORY] [-o FILE] [--dname FIELD]

Options:      
    -d DIRECTORY         Input directory [default: resources/results]   
    -o FILE              Output file [default: resources/analyzes/diff_language.pkl] 
    --dname FIELD        Diff Field Name[default: diff]
"""

import json
import glob
import os

from docopt import docopt
from tqdm import tqdm
import pickle
from collections import Counter
from p_tqdm import p_map
from helper import get_diff_languages

# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close




if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    

    output_tmp_directory = os.path.splitext(output_file)[0]
    
    os.makedirs(output_tmp_directory, exist_ok=True)


    diff_field_name = args['--dname']

    def diff_language(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            data = json.load(json_file)
            
            extensions = []
            for commit in data:
                extensions.append(get_diff_languages(commit, diff_field_name))
                
            with open(project_result_path, "wb") as result_file:
                pickle.dump(extensions, result_file)

    p_map(diff_language, input_files)

    print("Done with individual")
    extensions = []

    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')

        with open(project_result_path, 'rb') as f:
            extension = pickle.load(f)

        extensions.extend(extension)

    with open(output_file, 'wb') as fp:
        pickle.dump(extensions, fp)
    

    flatten_list = [element for sublist in extensions for element in sublist]
    c = Counter(flatten_list)

    languages = ['java', 'py', 'rb', 'php', 'go', 'js']


    print(f'Number of extensions: {len(extensions)}')
    d = []
    for l in languages:
        print(l)
        d.append(c[l])
        print(c[l] / len(extensions))
    print(sum(d)/len(extensions))

    print(c.most_common(1000))
    # I need java, py, rb, php, go, js




            

