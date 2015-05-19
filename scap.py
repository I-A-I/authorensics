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
        # return find_uni_ngrams(self.texts[0])
        # print map(lambda x : find_uni_ngrams(x), self.texts)
        self.ngrams = [list(a[0]) for a in zip(*map(lambda x : find_uni_ngrams(x), self.texts))]
        self.ngram_counters = map(lambda x : dict(Counter(x)), self.ngrams)
        return self.ngram_counters

    
    # Add multiple textsshell
    
    def add_texts(self, *new_texts):
        for new_text in new_texts:
            self.add_text(new_text)

    # For each n-gram, use the shorter profile for comparison
    # Similarity should probably be an _absolute_ measure of intersection
    # Not a proportion

def sort_text(ng_c):
    ngram = []
    
    for x in ng_c:
        pass
    pass

    
""" THIS IS USED FOR MAGNITUDE STUFF WHICH WE MIGHT NOT USE?!?!??!!?!?!? MAYBE INCLUDE FOR FUN

def find_intersection(p1, p2):
    # Finds the intersection of two dictionaries
    # Returns a dictionary
    d = {}
    for x in p1.keys():
        if x in p2.keys():
            d[x] = min([p1[x],p2[x]])
    return d


    
def find_distance(p1,p2):
    # Finds the distance between to dictionaries
    # Returns a magnitude. The higher the magnitude, the more similar
    tup = [x*x for x in find_intersection(p1,p2).values()]
    tup = sum(tup)
    tup = tup/(1.0*max([len(p1.keys()),len(p2.keys())]))
    return tup
"""
if __name__ == "__main__":
    s = Profile()
    s.add_text("this is a story about ziwei and his Agar.io :D\nHe is rlly gud at dat game. philipp has acheived nirvana. steven still has to deal with fb's bs. LOL That's some unicode for  you.")
    p = Profile()
    p.add_text("Today in period 7, our software development class, we finished the SCAP algorithm and are now waiting for Philipp to finish making the skeleton. Steven has been working arduosly on the frontend javascript. He is currently making a loading screen. Ziwei is reading a book")
    og = Profile()
    og.add_text("watsup homedog ziwei, how you doin. Philipp has achieved nirvana and is now doing stuff for a teacher. wut a good guy. steven is still working with fb. i hve nothign to do D: LOL")
    text = og.analyze_text()
    print text
    #print find_distance(text,text)
    #print find_distance(s.analyze_text(),text)
    #print find_distance(p.analyze_text(),text)
    text = \
"""






"""
