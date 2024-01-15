import re

def is_binary(commit, field = 'diff'):
    diff = commit[field]
    pattern = 'Binary files|old mode|new file mode|deleted file mode'
    return len(re.findall(pattern, diff)) >= 1

def is_bot(commit):
    pattern = 'bot'
    fields = ['author_email', 'author_name', 'committer_email', 'committer_name']
    
    for field in fields:
        if pattern in commit[field]:
            return True
    return False

def is_revert(commit, field='message'):
    pattern = '^Revert \"'        
    message = commit[field]
    return len(re.findall(pattern, message)) >= 1
    

trivial_messages = [
    'update changelog',
    'prepare version',
    'bump version',
    'modify makefile',
    'update submodule'    
]

def is_trivial(commit, field='message'):
    message = commit[field]
    for t_message in trivial_messages:
        if t_message in message.lower():
            return True
    return False    

path_to_pretrained_model = 'analyze/lid.176.bin'
fmodel = None


def get_message_language(commit, field='message'):
    global fmodel
    if fmodel is None:
        # Only import if required
        import fasttext
        fmodel = fasttext.load_model(path_to_pretrained_model)
    message = commit[field]
    
    # The specific fasttext model only returns one value
    language, confidence   =  fmodel.predict(message.replace('\n', ' '))
    assert len(language) == 1 and len(confidence) == 1

    return language[0].replace('__label__', ''), confidence[0]

CONFIDENCE_THRESHOLD = 0.5

def is_english(commit, field='message'):
    lang, confidence = get_message_language(commit, field)
    # Shows the best result
    return lang == 'en' and confidence > CONFIDENCE_THRESHOLD
    
def line_to_extension(line):
    file = [item for item in line.split(' ') if item.strip() != '']
    # take until first /
    res = []
    for item in reversed(file):
        if item != '/':
            res.append(item)
        else:
            break
    res = list(reversed(res))
    file = ''.join(res)
    
    if '.' in file:
        return file.split('.')[-1]
    else:
        return file.split('/')[-1]

def get_diff_languages(commit, field='diff'):
    pattern = '^diff --git a/.*'
    diff = commit[field]
    
    files_changed = re.findall(pattern, diff, re.MULTILINE)
    extensions = [line_to_extension(line) for line in files_changed]

    return extensions


def is_conventional_commit(commit, field='message'):
    pattern = '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)'
    diff = commit[field]

    return len(re.findall(pattern, diff)) >= 1


# Its more performant to work directly with the list
def get_sequence_length(commits:list, tokenizer, field='message', has_eos = True):
    assert isinstance(commits, list)
    if len(commits) == 0:
        return []

    texts = [commit[field] for commit in commits]
    tokenized = tokenizer(texts).input_ids
    lengths = [len(tokenized) for tokenized in tokenized]
    if has_eos:
        lengths = [length - 1 for length in lengths]

    return lengths
    
