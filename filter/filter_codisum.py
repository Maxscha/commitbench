# Takes json file and removes messages which are longer then n,m
# TODO GET INPUT OUTPUT message_max_length diff_max_length

#!/usr/bin/env python3
"""
Usage:
    filter.py [-h] [-m m] [-n n] [-f] [z] [-i FILE] [-o FILE]

Options:
    -h --help       Show this screen.
    -z              Only takes commits with dobj confirm messages (Also changes message filtering to msg_first_sentence)
    -m m            Max length for message sequence
    -n n            Max length for diff sequence
    -f --file       Processes single files instead of whole directory    
    -i FILE         Input file or folder(if directory is specified) [default: resources/result]
    -o FILE         Output file or folder(if directory is specified) [default: resources/result_tokenized]
"""

import json
import bigjson
import glob
import os
from nltk.tokenize import TweetTokenizer
from docopt import docopt
from tqdm import tqdm

if __name__ == '__main__':
    args = docopt(__doc__)
    # print(args)
    input_path = args["-i"]
    output_path = args["-o"]

    #Please ignore I know its dirty
    max_message_sequence = 1000000 if args["-m"] is None else int(args["-m"])
    max_diff_sequence = 1000000 if args["-n"] is None else int(args["-n"])


    if not args["--file"]:
        input_files = glob.glob(f'{input_path}/*.json')
        os.makedirs(output_path , exist_ok=True)
    else:
        input_files = [input_path]
        os.makedirs(os.path.dirname(output_path) , exist_ok=True)




    # # TODO ITERATE OVER EVERYTHING AND 
    # max_diff = 100
    # max_msg = 30


    for input_file in tqdm(input_files):
        repo_name = os.path.basename(input_file)
        if not args["--file"]:
            result_path = os.path.join(output_path, repo_name)
        else:
            result_path = output_path

        # is_msg_dobj -> To check
        # msg_first_sentence -> Split on space, filter based on m rename to message
        # diff_tokenized -> Split on space, filter based on n rename to diff_tokenized
        # hash -> Hash
         
        with open(input_file, 'rb') as json_file:
            data = bigjson.load(json_file)

            filtered_commits = []
            for commit in data:
                
                msg_len = len(commit["message"].split(' '))
                diff_len = len(commit["diff"].split(' '))
                if msg_len < max_message_sequence and diff_len < max_diff_sequence:
                    new_commit = {
                        "message": commit["message"],
                        "diff": commit["diff"],
                        "hash": commit["hash"]                        
                    }
                    filtered_commits.append(new_commit)                        
            with open(result_path, "w") as f:
                json.dump(filtered_commits, f)
            

            

