#!/usr/bin/env python
"""
Usage:
    get_repo_list.py [-d DATA_PATH] [-o OUTPUT] [-h]

Options:
    -h --help       Show this screen.
    -d DATA_PATH    [default: resources/data]
    -o OUTPUT       [default: resources/repos.txt]    
"""
import pickle
from docopt import docopt
import os
from tqdm import tqdm

if __name__ == '__main__':
    args = docopt(__doc__)
    data_path = args['-d']
    output = args['-o']
    list_of_projects = []

    for language in tqdm(('python', 'javascript', 'java', 'ruby', 'php', 'go')):
        with open(os.path.join(data_path, f'{language}_dedupe_definitions_v2.pkl'), "rb") as f:
            definitions = pickle.load(f)
            list_of_projects_per_language = list(set([definition["nwo"] for definition in definitions]))
        list_of_projects.extend(list_of_projects_per_language)

    list_of_projects = list(set(list_of_projects))

    with open(output, "w") as f:
        f.writelines([f'{project}\n' for project in list_of_projects])