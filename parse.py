#why is python such a good language?

#from nltk import brown
import re
import collections
from collections import Counter
import operator

emoticons = [ x.strip() for x in open("emoji.txt").readlines() ]
#CHECK EMOTICONS IN TOKENS


sentence = "A cat ate a dog in the           \n          forest!!!!!! >.< >////< XD so rundum.\n#LOL #SORRYNOTSORRY #TRUF"


PUNCTUATIONS = "!:\-,;.!?~"
punctuation_regex = re.compile("(?:([\w]+)([" + PUNCTUATIONS + "]+)\s?)")


#SPELL CHECKER STUFF BY PETER NORVIG//////////////////////////////////////////////////
def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('/usr/share/dict/american-english').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
#///////////////////////////////////////////////////////////////////////////////////////



def is_emoticon(s):
    return s in emoticons

def is_capitalized(s):
    return 0

def split_punctuations(tokens):
    new_tokens = []
    for token in tokens:
        match = re.match(punctuation_regex, token)
        if match:
            new_tokens.append(match.group(1))
            new_tokens.append(match.group(2))
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
        self.spelling_errors = []
        def dumb(x):
            self.spelling_errors.append(x)
            return x
        self.tokens = map(lambda x : dumb(x) if correct(x) != x, self.tokens)
        self.emoticons = []
        self.words = []
        map(lambda x : self.emoticons.append(x) if is_emoticon(x) else self.words.append(x), self.tokens)
        self.word_count = dict(Counter(self.words))
        self.emoticon_count = dict(Counter(self.emoticons))
        return [self.tokens, self.word_count, self.emoticon_count]

d = ChatParser(sentence)

print d.parseParser()

d.addFragment("gdi, you are so bhed\n Plz")

d.parseParser()

print d.tokens
