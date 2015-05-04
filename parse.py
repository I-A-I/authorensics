#why is python such a shitty language?

import nltk
import re
from collections import Counter
import operator

sentence = "A cat ate a dog in the                     forest!!!!!! >.< >////< XD so rundum."
emoticon_regex = re.compile('')
emoticon_unicode_regex = re.compile('')

PUNCTUATIONS = "!:\-,;.!?~"
punctuation_regex = re.compile("(?:([\w]+)([" + PUNCTUATIONS + "]+)\s)")

def is_emoticon(s):
    return 0

def is_capitalized(s):
    return 0

def split_punctuations(tokens):
    new_tokens = []
    for token in tokens:
        match = re.match(punctuation_regex, token)
        if match:
            new_tokens.append(match.group(0))
            new_tokens.append(match.group(1))
        else:
            new_tokens.append(token)
    return new_tokens

class ChatParser:
    def addFragment(self, new_frag):
        if new_frag != '':
            self.fragments.append(new_frag)

    def addFragments(self, new_frags):
        map(lambda x : self.fragments.append(x), new_frags.split('\n'))

    def __init__(self, fragment=''):
        self.fragments = []
        if '\n' in fragment:
            self.addFragments(fragment)
        else:
            self.addFragment(fragment)
    
    def parseParser(self):
        self.tokens = reduce(operator.add, map(lambda x : split_punctuations(x.split()), self.fragments))
        self.word_count = dict(Counter(self.tokens))   
        return [self.tokens, self.word_count]

d = ChatParser(sentence)

print d.parseParser()

print d.tokens
