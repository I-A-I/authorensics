import re
from collections import Counter
import operator
import string
import codecs

emoticons = [x.strip() for x in open("emoji.txt").readlines()]
sentence = "A cat ate a dog in the           \n          forest!!!!!! >.< >////< XD so rundum.\n#LOL #SORRYNOTSORRY #TRUF"

PUNCTUATIONS = "!:\-,;.!?~"
punctuation_regex = re.compile("(?:([\w]+)([" + PUNCTUATIONS + "]+)\s?)")

#Based on the spell checker by Peter Norvig//////////////////////////////////////////////////
NWORDS = codecs.open('/usr/share/dict/american-english', "r", "utf-8").read().split()

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
      self.emoticons = []
      self.words = []
      map(lambda x : self.emoticons.append(x) if is_emoticon(x) else self.words.append(x), self.tokens)
      def dumb(x):
         self.spelling_errors.append(x)
         return correct(x)
      self.words = map(lambda x : dumb(x) if x in correct(x) else x, self.words)
      self.spelling_count = dict(Counter(self.spelling_errors))
      self.word_count = dict(Counter(self.words))
      self.emoticon_count = dict(Counter(self.emoticons))
      return [self.word_count, self.emoticon_count, self.spelling_count]

# d = ChatParser(sentence)

# print d.parseParser()

# d.addFragment("gdi, you are so bhed\n Plz")

# d.parseParser()


# print d.tokens

print(correct('hii'))
