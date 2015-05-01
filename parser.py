import nltk.data, re

s = """
HELLO, I'm just messaging you
2 test if this parser
actually works. what is the math
hw? ^^ LOOOOOOL. what is speling
lololololololololol :D.
wat r sum other emoji i can use
:^) yeeeeeeeeeeeeee
is dis what fb chat looks like
i hope so
no.
twitch chat is muchworse
kappa
PJSalt
"""
s = " ".join(s.strip().split("\n"))
d = nltk.data.load("tokenizers/punkt/english.pickle")
l = [re.split("\s",x) for x in d.tokenize(s)]
print l
# print nltk.tokenize.punkt.PUNCTUATION
# detector = nltk.data.load("tokenizers/punkt/english.pickle")

# l = "\n----\n".join(detector.tokenize(s.strip()))
# print l
