#!/usr/bin/env python3
"""
Usage:
    tokenizer.py [-h] [-m] [-f] [-i FILE] [-o FILE]

Options:
    -h --help       Show this screen.
    -f --file       Processes single files instead of whole directory
    -m --multi      Uses multi-thread processing to speed up processing
    -i FILE         Input file or folder(if directory is specified) [default: resources/result]
    -o FILE         Output file or folder(if directory is specified) [default: resources/result_tokenized]
"""

import json
import glob
import os
from nltk.tokenize import TweetTokenizer
from docopt import docopt
from tqdm import tqdm

tknzr = TweetTokenizer()

def tokenize_text(text):
    # text = text.replace('\n', '')
    return tknzr.tokenize(text)

def tokenize_code(code):
    d = code.strip()
    d = d.replace('\n', '<nl>')
    d = d.replace("diff --git", "")
    d = d.replace('---', 'mmm') # Added because the original dataset does the same thing
    d = d.replace('+++', 'ppp') # Added because the original dataset does the same thing
    try:
        return tknzr.tokenize(d)
    except OverflowError as e:
        print(e)
        return None

if __name__ == '__main__':
    args = docopt(__doc__)
    # print(args)
    input_path = args["-i"]
    output_path = args["-o"]

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
        if os.path.exists(result_path):
            continue
        with open(input_file) as json_file:
            data = json.load(json_file)
            total = len(data)
            total_over_100 = 0
            for commit in data:
                if commit['diff'] is None or commit['message'] is None: #To prevent errors when commits where created without a diff (e.g. git commit --allow-empty)
                    continue
                    
                tokenized_code = tokenize_code(commit['diff'])
                
                #Sometimes the code can not be tokenized properly because nltk can't handle the tokenization of long numbers well. Should not happen for messages, hence why only code is checked
                if tokenized_code is None:
                    continue
                commit["diff_tokenized"] = ' '.join(tokenized_code)

                commit["message_tokenized"] = ' '.join(tokenize_text(commit['message']))
            # data = list([c for c in data if "diff_tokenized" in c.keys() and len(c["diff_tokenized"]) <= max_diff])
            data = list([c for c in data if "diff_tokenized" in c.keys()])

            with open(result_path, "w") as f:
                json.dump(data, f)
            

            

