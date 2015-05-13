from collections import Counter
import operator

# This is the Source Code Authorship Profile (SCAP) method
# Based primarily on "Identifying Authorship by Byte-Level N-Grams:The Source Code Author Profile (SCAP) Method"
# Publicly available at https://www.utica.edu/academic/institutes/ecii/publications/articles/B41158D1-C829-0387-009D214D2170C321.pdf

# The range of n-grams to use for profiling
N_GRAM_MIN = 2
N_GRAM_MAX = 6

#http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
def find_ngram(input_list, n):
    assert n >= 2
    return zip(*[input_list[i:] for i in xrange(n)])

def find_uni_ngrams(s):
    x = []
    for k in xrange(N_GRAM_MIN, N_GRAM_MAX+1):
        x.append(find_ngram(s, k))
    return x

# Class for author profile
class Profile:
    def __init__(self, name="", *rest_text):
        self.name = name
        self.texts = []
        if rest_text:
            apply(self.add_texts, rest_text)

    # Add a single text
    def add_text(self, new_text):
        self.texts.append(unicode(new_text,'utf-8'))

    # For every n-gram between N_GRAM_MIN and N_GRAM_MAX:
        # ... Count n-grams
        # ... Sort descendingly
        # ... Discard frequency to save memory (?)
    # Return array of arrays
    def analyze_text(self):
        self.ngrams = reduce(operator.add, reduce(operator.add, map(lambda x : find_uni_ngrams(x), self.texts)))
        self.ngram_counters = dict(Counter(self.ngrams))
        print(self.ngram_counters)

    # Add multiple textsshell
    
    def add_texts(self, *new_texts):
        for new_text in new_texts:
            self.add_text(new_text)

    # For each n-gram, use the shorter profile for comparison
    # Similarity should probably be an _absolute_ measure of intersection
    # Not a proportion
    
def find_distance(p1, p2):
    
