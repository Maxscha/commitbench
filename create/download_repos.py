#!/usr/bin/env python
"""
Usage:
    download_repos.py [-r REPO_LIST] [-o OUTPUT_DIRECTORY] [-h]

Options:
    -h --help               Show this screen.
    -r REPO_LIST            [default: resources/repos.txt]
    -o OUTPUT_DIRECTORY     [default: resources/repos/]    
"""
import pickle
from docopt import docopt
from tqdm import tqdm
from p_tqdm import p_map
import os

import requests
import pygit2

#50 repos ~ 200 mb

def download_repository(repository, output_directory):
    org, project = repository
    repo_url = f'https://github.com:/{org}/{project}.git'
    repo_path = os.path.join(output_directory, f'{org}/{project}')
    #TODO CHECK IF EXIST AND DECIDE WHAT HAPPENS THEN
    try:
        repo = pygit2.clone_repository(repo_url, repo_path, bare=True)
        return None
    except ValueError as error:
        #TODO THINK ABOUT RETRY AND LATEST MAYBE WE COULD JUST DO A GIT PULL INSTEAD?
        None
    except pygit2.GitError as error:
        print(f'{org}/{project}')
        print(error)
        return f'{org}/{project}'



if __name__ == '__main__':
    args = docopt(__doc__)
    repo_list = args['-r']
    print(repo_list)
    output_directory = args['-o']
    print(output_directory)

    with open(repo_list, "r") as f:
        repos = f.readlines()
        repos = [r.strip() for r in repos]
    
    print(repos[0])

    
    splitted = [(r.split("/")[0], r.split("/")[1]) for r in repos]
    res = list(p_map(lambda x: download_repository(x, output_directory), tqdm(splitted), num_cpus=20))

    res = ['f{r}\n' for r in res if r is not None]

    with open('resources/failed_repos.txt', 'w') as f:
        f.writelines(res)


