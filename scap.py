from collections import Counter
import math
import features

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
    # For each n-gram, use the shorter profile for comparison
    # Similarity should probably be an _absolute_ measure of intersection
    # Not a proportion

def sort_text(ng_c):
    #sorts the list of dictionaries of ngrams and returns the top 10 results
    ngram = []
    for x in ng_c:
        ngram.append(dict(sorted(x.items(), key=operator.itemgetter(1), reverse = True)[:10]))
    return ngram

def find_intersection(p1, p2):
    # Finds the intersection of two dictionaries
    # Returns a dictionary
    d = {x : min(p1[x], p2[x]) for x in p1 if x in p2}
    return d

def find_union(p1, p2):
    # Finds the union of two dictionaries
    # Returns a dictionary
    d = p1.copy()
    d.update(p2)
    return d

def find_distance(p1,p2):
    # Prevent division by zero
    if len(p1.keys()) == 0 or len(p2.keys()) == 0:
        return 0
    # Finds the distance between to dictionaries
    # Returns a magnitude. The higher the magnitude, the more similar
    tup = [x*x for x in find_intersection(p1,p2).values()]
    tup = sum(tup)
    tup = tup/(1.0*max([len(p1.keys()),len(p2.keys())]))
    return tup

def find_percent(p1,p2):
    # Finds the percentage similarity
    # |(p1 ^ p2)| / |(p1 U p2)|
    u = find_union(p1,p2)
    if len(u.keys()) == 0:
        return 0
    return find_distance(p1,p2) / find_distance(u,u)

def parseParser(profile):
  def get_if_error(x):
     profile.spelling_errors.append(x)
     return features.correct(x)
  profile.tokens = sum(map(lambda x : features.split_punctuations(x.split()), profile.fragments))
  profile.spelling_errors = []
  profile.emoticons = []
  profile.words = []
  map(lambda x : profile.emoticons.append(x) if features.is_emoticon(x) else profile.words.append(x), profile.tokens)
  profile.words = map(lambda x : get_if_error(x) if x in correct(x) else x, profile.words)
  profile.spelling_count = dict(Counter(profile.spelling_errors))
  profile.word_count = dict(Counter(profile.words))
  profile.emoticon_count = dict(Counter(profile.emoticons))
  return [profile.word_count, profile.emoticon_count, profile.spelling_count]

def find_all_percents(p1, p2):
    # Finds all the percent similarites between lists of ngrams
    return [find_percent(x[0],x[1]) for x in zip(p1,p2)]

def format_number(percent):
    return math.ceil(percent * 100) / 100

def find_dumb_score(l):
    # "Mathematically and Scientifically" figures out how to compare the percents
    # Deserves a Turing Award
    # 6-grams are worth more than 2-grams
    return sum([l[0]*2,l[1]*3,l[2]*4,l[3]*5,l[4]*6])

def get_ngram_counters(profile):
    profile.ngrams = [list(a[0]) for a in zip(*map(lambda x : find_uni_ngrams(x), profile.texts))]
    profile.ngram_counters = map(lambda x : dict(Counter(x)), profile.ngrams)
    return profile.ngram_counters


def compare_profiles_scap(p1, p2):
    return find_all_percents(get_ngram_counters(p1), get_ngram_counters(p2))
    #result = find_dumb_score(find_all_percents(p1.get_ngram_counters(), p2.get_ngram_counters()))
    #result = format_number(result)
    #return result


def analyze(anon_profile, candidate_profiles):
    results = {}
    for candidate_name, candidate_profile in candidate_profiles.iteritems():
        result = compare_profiles_scap(anon_profile, candidate_profile)
        results[candidate_name] = result

    return results
