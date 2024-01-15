#!/usr/bin/env python3
"""
Usage:
    enhance.py [-h] [-i FILE] [-o FILE]

Options:
    -h --help                           Show this screen.
    -i FILE                             Input file or folder(if directory is specified) [default: resources/results]
    -o FILE                             Output file or folder(if directory is specified) [default: resources/results_enhanced]
"""

import json
import glob
import os
from docopt import docopt



from p_tqdm import p_map
from helper import replace_version_number, replace_issue, remove_git_meta, replace_urls, remove_email

def main():
    args = docopt(__doc__)
    
    input_path = args["-i"]
    output_path = args["-o"]
    
    input_files = glob.glob(f'{input_path}/*.json')
    os.makedirs(output_path , exist_ok=True)

    def enhance_file(input_file):    
        repo_name = os.path.basename(input_file)

        result_path = os.path.join(output_path, repo_name)
        if os.path.exists(result_path):
            return

         
        with open(input_file, 'rb') as json_file:            

            data = json.load(json_file)  
            enhanced_commits = []
            
            message_field = 'message'
            diff_field = 'diff'

            for commit in data:
                commit[message_field] = replace_issue(commit[message_field])
                commit[message_field] = replace_version_number(commit[message_field])
                commit[message_field] = replace_urls(commit[message_field])
                commit[message_field] = remove_email(commit[message_field])


                commit[diff_field] = remove_git_meta(commit[diff_field])

                # enhancer sometimes returns empty strings which is okay
                if commit[message_field] == '' or commit[message_field] == 'null':
                    continue
                enhanced_commits.append(commit)   

            
            with open(result_path, "w") as f:
                json.dump(enhanced_commits, f)
            
            return (len(data), len(enhanced_commits))
            
    result = p_map(enhance_file, input_files, num_cpus=12)



if __name__ == '__main__':
    main()
