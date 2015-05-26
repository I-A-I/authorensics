import re
from collections import Counter
import string
import codecs

emoticons = [x.strip() for x in open("emoji.txt").readlines()]

PUNCTUATIONS = "!:\-,;.!?~"
punctuation_regex = re.compile("(?:([\w]+)([" + PUNCTUATIONS + "]+)\s?)")

#Based on the spell checker by Peter Norvig//////////////////////////////////////////////////
try:
    NWORDS = codecs.open('/usr/share/dict/american-english', "r", "utf-8").read().split()
except:
    NWORDS = codecs.open('/usr/share/dict/words', "r", "utf-8").read().split()


def edits(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in string.ascii_lowercase if b]
   inserts    = [a + c + b     for a, b in splits for c in string.ascii_lowercase]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return list(set(e2 for e1 in edits(word) for e2 in edits(e1) if e2 in NWORDS))

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits(word)) or known_edits2(word) or [word]
    return candidates
#///////////////////////////////////////////////////////////////////////////////////////

def is_emoticon(s):
    return s in emoticons

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
