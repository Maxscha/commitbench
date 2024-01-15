from pickle import GLOBAL
import re

from segtok.segmenter import split_single
from flair.data import Sentence
from flair.models import SequenceTagger

# 'diff --git' -> Remve as well
# Index index 2f4c4da..af8dc16 100644 -> Always second row remove it

def remove_git_meta(diff):
    # lines = diff.split('\n')
    # lines[0] = lines[0].replace('diff --git', '')
    # diff = '\n'.join(lines)

    pattern  = r"index [a-z0-9]{7}\.\.[a-z0-9]{7}"
    return re.sub(pattern, 'index <HASH>..<HASH>', diff, flags=re.MULTILINE)

# Find ISsues
#\w+ and replace them with <ISSUE>
def replace_issue(text):
    return re.sub(r'v?[\d+\.]+(\d)', "<I>", text)

# FIND VERSION  
# AND CONVERT TO VERSION

# [\d+\.]+(\d)
def replace_version_number(text):
    return re.sub(r'v?[\d+\.]+(\d)', "<V>", text)

    # FIND VERSION  
# AND CONVERT TO VERSION

# [\d+\.]+(\d)
def replace_urls(text):
    return re.sub(r'https?:\/\/\S+\.[^()]+(?:\([^)]*\))*', "<URL>", text)

def remove_email(text):
    pattern = r"((co\-)?authored\-by|signed\-off[\-\s]by|contributed\-by|author\:|reviewed\-by|change\son|thanks\sto|reviewed\sby|approved\sby|patch:|signed\soff|tested[\s|\-]by|submitted\sby|reported\-by|suggested\-by|paired\-with)(.*\@.*)$"
    result = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL).strip()

    pattern = r"([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"
    result = re.sub(pattern, '<EMAIL>', result, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)
    return result

tagger = None

# Can deadlock if called from multiple threads
def replace_name(text):
    global tagger
    if tagger is None:
        tagger = SequenceTagger.load("flair/ner-english")
    sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
    tagger.predict(sentences)

    found = []
    for sent in sentences:
            for entity in sent.get_spans('ner'):
                if entity.tag == 'PER' and entity.score > 0.95 and ' ' in entity.text:
                    found.append(entity)
    
    for entity in found:
        text = text.replace(entity.text, '<NAME>')
    return text
    
    