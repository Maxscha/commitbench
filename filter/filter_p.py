#!/usr/bin/env python3
"""
Usage:
    filter_p_new.py [-h] [--m_max m] [--m_min m] [--d_max d] [-t TOKENIZER] [-f] [-i FILE] [-o FILE] [--language_msg] [--language_diff] [--language_diff_endings ENDINGS] [--language_diff_percentage P] [--binary] [--revert] [--trivial] [--bot]

Options:
    -h --help                           Show this screen.    
    --m_max m                           Max length for message sequence
    --m_min m                           Min length for message sequence
    --d_max d                           Max length for diff sequence
    -t TOKENIZER                        Tokenizer to use [default: t5-small]
    -f --file                           Processes single files instead of whole directory    
    -i FILE                             Input file or folder(if directory is specified) [default: resources/results_dobjs]
    -o FILE                             Output file or folder(if directory is specified) [default: resources/results_filtered]
    --language_msg                      Filters out non english messages
    
    --language_diff                     Diff needs to include file ending from option --language_diff_endings
    --language_diff_endings ENDINGS     Endings which should be considers as allowed file endings, seperated with a comma [default: java,py,rb,php,go,js]
    --language_diff_percentage P        If language_diff is enabled this determines how many percent ot endings in a diff need to be in allowed endings [default: 0.5]
    
    --binary                            Filters out binary diffs
    --revert                            Filters out revert messages
    --trivial                           Filters out trivial messages
    --bot                               Filters out bot messages
"""

import json
import glob
import os
from docopt import docopt
import re

from helper import *
from p_tqdm import p_map
from tqdm import tqdm

from transformers import AutoTokenizer
from transformers.utils import logging
logging.set_verbosity(40)

model = None



def is_not_english_message(message):
    prediction =  model.predict(message.replace('\n', ''))
    lang = prediction[0][0].replace('__label__', '')
    confidence = prediction[1][0]
    return lang != 'en' and confidence > 0.8


def is_min_diff_language(commit, field, allowed_endings, min_percentage = 0.5):
    extensions = get_diff_languages(commit, field)

    allowed_extensions =[e for e in extensions if e in allowed_endings]

    p = 0

    if len(extensions) == 0:
        p = 0
    else:
        p =len(allowed_extensions) / len(extensions)
        
    return p > min_percentage


        

def main():
    args = docopt(__doc__)
    
    input_path = args["-i"]
    output_path = args["-o"]

    tokenizer = AutoTokenizer.from_pretrained(args['-t'])


    #Please ignore I know its dirty
    min_message_sequence = 0 if args["--m_min"] is None else int(args["--m_min"])
    max_message_sequence = 1000000 if args["--m_max"] is None else int(args["--m_max"])
    max_diff_sequence = 1000000 if args["--d_max"] is None else int(args["--d_max"])    

    if not args["--file"]:
        input_files = glob.glob(f'{input_path}/*.json')
        os.makedirs(output_path , exist_ok=True)
    else:
        input_files = [input_path]
        os.makedirs(os.path.dirname(output_path) , exist_ok=True)

    def filter_file(input_file):    
        repo_name = os.path.basename(input_file)
        if not args["--file"]:
            result_path = os.path.join(output_path, repo_name)
            if os.path.exists(result_path):
                return
        else:
            result_path = output_path
         
        with open(input_file, 'rb') as json_file:            

            data = json.load(json_file)  
            filtered_commits = []
            
            message_field = 'message'
            diff_field = 'diff'

            message_sequence_length = get_sequence_length(data, tokenizer, message_field)
            diff_sequence_length = get_sequence_length(data, tokenizer, diff_field)

            for commit, message_length, diff_length in zip(data, message_sequence_length, diff_sequence_length):
                if message_length < min_message_sequence:
                    continue

                if message_length > max_message_sequence or diff_length > max_diff_sequence:
                    continue     
                    

                if args['--language_diff']:
                    endings = args['--language_diff_endings'].split(',')
                    percentage = float(args['--language_diff_percentage'])
                    if not is_min_diff_language(commit, diff_field, endings, percentage):
                        continue

                
                if args['--bot']:
                    if is_bot(commit):
                        continue
                
                if args['--binary']:
                    if is_binary(commit, field = diff_field):
                        continue
                
                if args['--language_msg']:
                    if not is_english(commit, field = message_field):
                        continue
                    
                if args['--revert']:
                    if is_revert(commit, field = message_field):
                        continue
                
                if args['--trivial']:
                    if is_trivial(commit, field=message_field):
                        continue

                
                    
                filtered_commits.append(commit)   

            
            with open(result_path, "w") as f:
                json.dump(filtered_commits, f)
            
            return (len(data), len(filtered_commits))
            
    result = map(filter_file, tqdm(input_files))
    result = list(result)
    



if __name__ == '__main__':
    main()
