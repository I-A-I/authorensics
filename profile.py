from collections import Counter
import features
import scap

# Class for author profile
class Profile:
    def __init__(self, *rest_text):
        self.texts = []
        if rest_text:
            apply(self.add_texts, rest_text)

    # Add a single text
    def add_text(self, new_text):
        # self.texts.append(unicode(new_text,'utf-8'))
        self.texts.append(new_text)

    # For every n-gram between N_GRAM_MIN and N_GRAM_MAX:
        # ... Count n-grams
        # ... Sort descendingly
        # ... Discard frequency to save memory (?)

    # Return array of arrays
    def get_ngram_counters(self):
        self.ngrams = [list(a[0]) for a in zip(*map(lambda x : scap.find_uni_ngrams(x), self.texts))]
        self.ngram_counters = map(lambda x : dict(Counter(x)), self.ngrams)
        return self.ngram_counters

    # Add multiple textsshell    
    def add_texts(self, *new_texts):
        for new_text in new_texts:
            self.add_text(new_text)

    def parseParser(self):
      def get_if_error(x):
         self.spelling_errors.append(x)
         return features.correct(x)
      self.tokens = sum(map(lambda x : features.split_punctuations(x.split()), self.fragments))
      self.spelling_errors = []
      self.emoticons = []
      self.words = []
      map(lambda x : self.emoticons.append(x) if features.is_emoticon(x) else self.words.append(x), self.tokens)
      self.words = map(lambda x : get_if_error(x) if x in correct(x) else x, self.words)
      self.spelling_count = dict(Counter(self.spelling_errors))
      self.word_count = dict(Counter(self.words))
      self.emoticon_count = dict(Counter(self.emoticons))
      return [self.word_count, self.emoticon_count, self.spelling_count]
