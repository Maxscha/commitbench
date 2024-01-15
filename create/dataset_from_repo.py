#!/usr/bin/env python
"""
Usage:
    dataset_from_repo.py [-r REPO_PATH] [-o OUTPUT_DIRECTORY] [-h]

Options:
    -h --help               Show this screen.
    -r REPO_PATH            [default: resources/repos]
    -o OUTPUT_DIRECTORY     [default: resources/result]
"""

import pygit2
import glob
from tqdm import tqdm
import json
import os
import sys
from docopt import docopt
import pickle as pk
from p_tqdm import p_map

def get_size_mb(data):
    return sys.getsizeof(data) / 1024.0 / 1024.0


def get_commit_description(repository, commit):
    if len(commit.parents) != 1:
        # No first commits, no merge commits, no commits with more than one parent (e.g. three-way-merge )
        return None
    d = repository.diff(commit.parents[0], commit)

    try:
        return {
            "hash": commit.hex,
            "diff": d.patch.strip(),
            "message": commit.message.strip(),
            'author_email': commit.author.email,
            'author_name': commit.author.name,
            'committer_email': commit.committer.email,
            'committer_name': commit.committer.name
        }
    #Only happens once in the whole dataset
    except LookupError as err:
        return None
    #Only happens once in the whole dataset skip as well
    except UnicodeDecodeError as err:
        return None

def is_repository_empty(repository):
    return list(repository.branches.local) == []


def get_all_commits(repository):
    if is_repository_empty(repository):
        return []

    head_commit = repository[repository.head.target]
    queue = [head_commit]
    done = []

    while len(queue) > 0:
        current_commit = queue.pop(0)

        for parent in current_commit.parents:
            if parent not in done and parent not in queue:
                queue.append(parent)
        done.append(current_commit)

    return done


def process_repo(repo_path, output_path):
    total_commits = 0
    commits_with_one_parent = 0
    commits_with_two_parents = 0
    commits_with_three_or_more_parents = 0
    commits_with_one_parent_to_big = 0
    used_commits = 0

    (base, name) = os.path.split(repo_path)
    (base, org) = os.path.split(base)
    result_path = f'{output_path}/{org}_{name}.json'

    if os.path.exists(result_path):
        return

    r = pygit2.Repository(repo_path)

    all_commits = [c for c in get_all_commits(r)]
    total_commits = len(all_commits)

    one_parent_commits = [c for c in all_commits if len(c.parents) == 1]
    commits_with_one_parent = len(one_parent_commits)

    two_parent_commits = [c for c in all_commits if len(c.parents) == 2]
    commits_with_two_parents = len(two_parent_commits)

    three_parent_commits = [c for c in all_commits if len(c.parents) > 2]
    commits_with_three_or_more_parents = len(three_parent_commits)

    

    result_commits = []
    for c in one_parent_commits:

        des = get_commit_description(r, c)
        # Removes to big of descriptions, will be removed anyway later
        if des is None:
            continue
        if (get_size_mb(des["diff"]) < 0.5):
            result_commits.append(des)
        else:
            commits_with_one_parent_to_big += 1

    used_commits = len(result_commits)

    with open(result_path, 'w') as fp:
        json.dump(result_commits, fp)

    return (total_commits, commits_with_one_parent, commits_with_two_parents, commits_with_three_or_more_parents, commits_with_one_parent_to_big, used_commits)


def main():
    args = docopt(__doc__)
    repos_path = args['-r']
    output_path = args['-o']
    print(repos_path)
    os.makedirs(output_path, exist_ok=True)
    repos = glob.glob(f'{repos_path}/*/*')    

    print(len(repos))

    statistics = []
    statistics = list(p_map(lambda x: process_repo(x, output_path), repos, num_cpus=0.5))

    with open(f'{output_path}_statistics.pk', 'wb') as fp:
        pk.dump(statistics, fp)

    print(f'Commits in {len(repos)} repos')


if __name__ == '__main__':
    main()
