#!/usr/bin/env python3
"""
Usage:
    author_counter.py [-d DIRECTORY] [-o FILE]

Options:      
    -d DIRECTORY         Input directory [default: resources/results]   
    -o FILE              Output file [default: resources/analyzes/author_counter.py]     
"""

import json
import glob
import os

from docopt import docopt
import pickle
from collections import Counter
from p_tqdm import p_map


# Get list of processed_repos in folder
# for each file: Open: Read number of commits, put in dict, close


if __name__ == '__main__':
    args = docopt(__doc__)
    
    input_directory = args["-d"]    
    input_files = glob.glob(f'{input_directory}/*.json')                     

    output_file = args['-o']    

    output_tmp_directory = os.path.splitext(output_file)[0]
    
    os.makedirs(output_tmp_directory, exist_ok=True)

    def author_counter(input_file):        
        repo_name = os.path.basename(input_file).replace('.pkl', '')
        
        project_result_path = os.path.join(output_tmp_directory, f'{repo_name}.pkl')
        if os.path.exists(project_result_path):
            return

        with open(input_file) as json_file:
            data = json.load(json_file)
            authors = [commit['author_email'] for commit in data]
            with open(project_result_path, "wb") as result_file:
                pickle.dump(authors, result_file)
            return authors

    all_authors = p_map(author_counter, input_files)

    counter = Counter()
    for authors in all_authors:
        counter.update(authors)

    print(counter.most_common(10))
    




            

