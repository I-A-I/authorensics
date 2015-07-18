'''
TO-DO
1. (DONE) Write generate_sample
2. (DONE) Get linear model working
3. (DONE )Implement feature extraction
4. (DONE) Implement algos #4, 5
5. Visualization?
'''


from profile import Profile
from math import log10
from math import floor
from time import time
import operator
import copy
import numpy as np
import nltk

# The maximum number of n-grams to use
MAX_GRAM = 8

# This is the Visualizable Evidence-Driven Approach (VEA)
# Described in their paper by Steven H. H. Ding, C. M. Fung, and Mourad Debbabi

# Each modality--word, character, part of speech--gets an event
# This event will contain data like author scores and confidence
# It contains EvidenceUnit instances
class Event:
    def __init__(self, modality, num_authors):
        self.modality = modality
        self.confidence = None
        self.scores = [None] * num_authors
        self.evidence_units = []
        self.prediction_index = None

    def add_eu(self, evidence_unit):
        self.evidence_units.append(evidence_unit)

# An evidence unit is ONE feature (one word, one character)
# It is contained in an Event instance
class EvidenceUnit:
    def __init__(self, feature, modality, num_authors):
        self.modality = modality
        self.feature = feature
        self.num_authors = num_authors
        self.scores = [None] * num_authors
        self.idf = 0
    
    # Determine the overall discriminant power of a feature
    # Used in algorithm #2
    def calculate_idf(self, candidates):
        authors_ever_used = 0
        for candidate in candidates:
            if candidate.find_feature(self.feature):
                authors_ever_used += 1

        constant = 0.1
        num_authors = len(candidates)

        self.idf = log10(float(num_authors) / (constant + authors_ever_used))


# Example: If modality is "word", content could be "it is" and length "2"
class Feature:
    def __init__(self, content, length, modality, frequency):
        self.content = content
        self.length = length
        self.modality = modality
        self.frequency = frequency

# Profile is the class used by the server
# VEAProfile is adapted for this algorithm's purposes
class VEAProfile(Profile):
    def __init__(self, profile):
        self.single_text = profile.single_text
        self.texts = profile.texts

        self.features = {}

    # Find matching feature in features array
    def find_feature(self, feature):
        features_of_modality = self.features[feature.modality]

        for self_feature in features_of_modality:
            if self_feature.content == feature.content:
                return self_feature
        
        return None

    # Find feature with greatest frequency
    # Used for TF
    def find_max_feature_frequency(self, modality, length):
        features_of_modality = self.features[modality]
        features_of_length = [feature for feature in features_of_modality if feature.length == length]

        max_frequency = 0
        for feature in features_of_length:
            if feature.frequency > max_frequency:
                max_frequency = feature.frequency

        return max_frequency

    # Used by algorithm #3
    # We're doing a 10-fold cross-validation test
    # If fold_number = 0, return first 10% of samples
    # as testing, last 90% of samples as training
    def generate_fold_samples(self, fold_number):
        # If number of texts is divisible by 10, things are easy
        # We don't need to break up any samples
        if len(self.texts) % 10 == 0:
            test_group_len = len(self.texts) / 10
            test_group_min = fold_number * test_group_len
            test_group_max = fold_number * test_group_len + test_group_len

            test_group = self.texts[test_group_min:test_group_max]
            training_group = self.texts[0:test_group_min] + self.texts[test_group_max:]

        # If number of texts is NOT divisible by 10, add all the samples together
        # And divide them into 10 slices
        else:
            # First, find length of one slice
            num_chars = len(self.single_text)
            if num_chars % 10 == 0:
                slice_len = num_chars / 10
            else:
                # In this case, the last slice will be slightly longer than the other slices
                slice_len = int(floor(num_chars / 10.))

            # Now generate indices of groups
            test_group_min = fold_number * slice_len
            test_group_max = fold_number * slice_len + slice_len
            
            test_group = self.single_text[test_group_min:test_group_max]
            training_group = self.single_text[0:test_group_min] + self.single_text[test_group_max:]
            
        return test_group, training_group


def extract_word_features(profile):
    text = profile.single_text
    raw_features = nltk.word_tokenize(text)
    feature_frequencies = {}

    for length in range(1, MAX_GRAM + 1):
        left = 0
        right = length

        while right <= len(raw_features):
            feature = " ".join(raw_features[left:right])
            if feature in feature_frequencies:
                feature_frequencies[feature] += 1
            else:
                feature_frequencies[feature] = 1

            left += 1
            right += 1


    all_features = []
    for feature_content, feature_frequency in feature_frequencies.iteritems():
        feature_modality = "word"
        feature_length = len(feature_content.split(" "))
        new_feature = Feature(feature_content, feature_length, feature_modality, feature_frequency)
        all_features.append(new_feature)

    return all_features

def extract_character_features(profile):
    text = profile.single_text
    feature_frequencies = {}

    for length in range(1, MAX_GRAM + 1):
        left = 0
        right = length
        while right < len(text):

            feature = text[left:right]
            if feature in feature_frequencies:
                feature_frequencies[feature] += 1
            else:
                feature_frequencies[feature] = 1

            left += 1
            right += 1


    all_features = []
    for feature_content, feature_frequency in feature_frequencies.iteritems():
        feature_modality = "character"
        feature_length = len(feature_content)
        new_feature = Feature(feature_content, feature_length, feature_modality, feature_frequency)
        all_features.append(new_feature)

    return all_features

# When n-grams were rearranged from word_features, total computation time for 
# one text was 33.8 seconds
def extract_pos_features(profile):
    text = profile.single_text
    tagged_text = nltk.word_tokenize(text)
    raw_features = nltk.pos_tag(tagged_text)
    feature_frequencies = {}

    for length in range(1, MAX_GRAM + 1):
        left = 0
        right = length
        while right < len(raw_features):
            ngram = raw_features[left:right]
            parts_of_speech = [pair[1] for pair in ngram]
            feature = " ".join(parts_of_speech)
            if feature in feature_frequencies:
                feature_frequencies[feature] += 1
            else:
                feature_frequencies[feature] = 1

            left += 1
            right += 1

    all_features = []
    for feature_content, feature_frequency in feature_frequencies.iteritems():
        feature_modality = "pos"
        feature_length = len(feature_content.split(" "))
        new_feature = Feature(feature_content, feature_length, feature_modality, feature_frequency)
        all_features.append(new_feature)

    return all_features


def construct_event(features, modality, num_authors):
    event = Event(modality, num_authors)
    for feature in features:
        eu = EvidenceUnit(feature, modality, num_authors)
        event.add_eu(eu)

    return event

# ALGORITHM 1
def create_event(candidate_profiles, anon_profile, modality):
    num_authors = len(candidate_profiles)
    if modality == "word":
        word_features = extract_word_features(anon_profile)
        anon_profile.features["word"] = word_features
        word_event = construct_event(word_features, "word", num_authors)
        return word_event

    if modality == "character":
        character_features = extract_character_features(anon_profile)
        anon_profile.features["character"] = character_features
        character_event = construct_event(character_features, "character", num_authors)
        return character_event

    if modality == "pos":
        pos_features = extract_pos_features(anon_profile)
        anon_profile.features["pos"] = pos_features
        pos_event = construct_event(pos_features, "pos", num_authors)
        return pos_event


def create_events(candidate_profiles, anon_profile):
    num_authors = len(candidate_profiles)
    events = []
    anon_profile = VEAProfile(anon_profile)
    modalities = ("word", "character", "pos")
    for modality in modalities:
        new_event = create_event(candidate_profiles, anon_profile, modality)
        events.append(new_event)
    
    return events, anon_profile


def tf(feature, candidate):
    modality = feature.modality
    length = feature.length

    candidate_feature = candidate.find_feature(feature)
    if (candidate_feature):
        frequency = candidate_feature.frequency
    else:
        frequency = 0

    max_feature_frequency = candidate.find_max_feature_frequency(modality, length)
    if max_feature_frequency == 0:
        return 0

    return float(frequency) / max_feature_frequency

# Find word, character, POS features in candidates
def extract_candidate_features(candidate_profiles, events, convert_to_vea=True):
    # this mode is not used by testing
    if convert_to_vea:
        candidates = []
        for name, candidate_profile in candidate_profiles.iteritems():
            candidate = VEAProfile(candidate_profile)

            candidate.features["word"] = extract_word_features(candidate)
            candidate.features["character"] = extract_character_features(candidate)
            candidate.features["pos"] = extract_pos_features(candidate)

            candidates.append(candidate)

    # this mode is used by testing
    else:
        candidates = []
        for candidate in candidate_profiles:
            candidate.features["word"] = extract_word_features(candidate)
            candidate.features["character"] = extract_character_features(candidate)
            candidate.features["pos"] = extract_pos_features(candidate)

            candidates.append(candidate)

    for index, event in enumerate(events):
        for eu_index, eu in enumerate(event.evidence_units):
            eu.calculate_idf(candidates)
            events[index].evidence_units[eu_index] = eu

    return candidates

# ALGORITHM 2
def score_event(event, anon_profile, candidates):
    # Lines 2-5
    # Score each feature based on TF for anon_profile
    anon_scores = []
    for eu in event.evidence_units:
        feature_score = tf(eu.feature, anon_profile)
        anon_scores.append(feature_score)

    # Lines 6-13
    # Score each feature based on TF-IDF for candidates
    for index, candidate in enumerate(candidates):
        candidate_scores = []
        for eu_index, eu in enumerate(event.evidence_units):
            score = tf(eu.feature, candidate) * eu.idf
            eu.scores[index] = score * anon_scores[eu_index]
            candidate_scores.append(score)

        dot_product = sum(map(operator.mul, anon_scores, candidate_scores))
        event.scores[index] = dot_product

    max_score = max(event.scores)
    event.prediction_index = event.scores.index(max_score)


def score_events(events, anon_profile, candidates):
    for event in events:
        score_event(event, anon_profile, candidates)

# Needed for Algorithm 3
# Return testing group and training group (containing profiles)
# Given the fold #
def generate_fold_groups(fold_number, candidates):
    testing_group, training_group = [], []
    for candidate in candidates:
        testing_sample, training_sample = candidate.generate_fold_samples(fold_number)

        testing_profile = VEAProfile(Profile(testing_sample))
        testing_group.append(testing_profile)

        training_profile = VEAProfile(Profile(training_sample))
        training_group.append(training_profile)

    return testing_group, training_group

# ALGORITHM 3
'''
For each event...
    Divide each candidate's samples into 10 groups
    Collate these 10 groups of every author into 10 supergroups, each containing each writer
    For every supergroup...
        testing_group = supergroup
        training_group = all supergroups except this one
        For every author_sample in testing_group:
            anon_profile = author_sample
            candidate_profiles = samples from training_group
            run algos #1 and #2 on them
            keep track of whether predicted author is actual author
            collect sample
        collect samples
    build linear model from samples
    using samples of real event, predict confidence
'''
def author_is_correct(event, real_author_index):
    # Find predicted author
    predicted_author_index = -1
    for index, score in enumerate(event.scores):
        if predicted_author_index == -1 or score > event.scores[predicted_author_index]:
            predicted_author_index = index

    return predicted_author_index == real_author_index

def find_second_highest(array):
    if len(array) < 1:
        raise Exception()
    
    elif len(array) == 1:
        return 0

    array_copy = copy.copy(array)
    max_index = array_copy.index(max(array_copy))
    del array_copy[max_index]

    return max(array_copy)

'''Table II
- average score
- max score
- min score
- distance(max to runner-up)
- num tokens in doc
- num tokens shared between doc and docs
'''
# The sample is used to build a linear model, to estimate confidence
def generate_sample(event, anonymous_doc, candidates):
    sample = []
    scores = event.scores

    average_score = sum(scores) / float(len(scores))
    sample.append(average_score)
    
    max_score = max(scores)
    sample.append(max_score)

    min_score = min(scores)
    sample.append(min_score)

    runner_up = find_second_highest(scores)
    distance = max_score - runner_up
    sample.append(distance)

    num_tokens = len(event.evidence_units)
    sample.append(num_tokens)

    anonymous_tokens = anonymous_doc.features[event.modality]
    anonymous_tokens = [feature.content for feature in anonymous_tokens]

    candidate_token_pool = []
    for candidate in candidates:
        for feature in candidate.features[event.modality]:
            if feature.content not in candidate_token_pool:
                candidate_token_pool.append(feature.content)

    shared_tokens = list(set(anonymous_tokens) & set(candidate_token_pool))
    num_shared_tokens = len(shared_tokens)
    sample.append(num_shared_tokens)

    return sample

def build_model(samples):
    inputs = []
    # Remove last dimension
    for sample in samples:
        input_ = sample[:-1]
        input_ = np.array(input_)
        inputs.append(input_)
    inputs = np.array(inputs)

    targets = []
    for sample in samples:
        targets.append(sample[-1])
    targets = np.array(targets)

    model = np.linalg.lstsq(inputs, targets)
    return model

def predict(model, sample):
    coefficients = model[0]
    precision_estimate = 0
    for index, coefficient in enumerate(coefficients):
        precision_estimate += coefficient * sample[index]

    return precision_estimate

# Algorithm 3
def estimate_confidence(events, anon_profile, candidates):
    samples = []
    for event in events:
        for fold_number in range(10):
            correct_guess = 0
            fold_samples = []
            testing_group, training_group = generate_fold_groups(fold_number, candidates)

            # lines 6-16
            for author_index, test_doc in enumerate(testing_group):
                # of type Profile
                candidate_profiles = copy.copy(training_group)

                test_event = create_event(candidate_profiles, test_doc, event.modality)

                # of type VEAProfile
                candidates_temp = extract_candidate_features(candidate_profiles, [test_event], convert_to_vea=False)
                score_event(test_event, test_doc, candidates_temp)

                if author_is_correct(test_event, author_index):
                    correct_guess += 1

                sample = generate_sample(test_event, test_doc, candidates_temp)
                fold_samples.append(sample)
            
            # lines 17-20
            precision = correct_guess / len(testing_group)
            for sample in fold_samples:
                sample.append(precision)

            # line 21
            samples += fold_samples

        model = build_model(samples)
        estimated_confidence = predict(model, generate_sample(event, anon_profile, candidates))
        event.confidence = estimated_confidence

# Algorithm 4
def normalize_scores(events):
    for event in events:
        confidence = event.confidence
        event.scores = [score * confidence for score in event.scores]
        for index, eu in enumerate(event.evidence_units):
            eu.scores = [score * confidence for score in eu.scores]
            event.evidence_units[index] = eu

# Algorithm 5
def combine_events(events, candidates):
    final_scores = [0] * len(candidates)
    for event in events:
        for index, score in enumerate(event.scores):
            final_scores[index] += score

    max_score = max(final_scores)
    author_index = final_scores.index(max_score)

    max_confidence = 0
    for event in events:
        if event.prediction_index == author_index:
            if event.confidence > max_confidence:
                max_confidence = event.confidence

    return (author_index, max_confidence)



def analyze(anon_profile, candidate_profiles):
    events, anon_profile = create_events(candidate_profiles, anon_profile)
    print "create_events"

    candidates = extract_candidate_features(candidate_profiles, events)
    print "extract_candidate_features"

    score_events(events, anon_profile, candidates)
    print "score_events"

    estimate_confidence(events, anon_profile, candidates)
    print "estimate_confidence"

    normalize_scores(events)
    print "normalize_scores"

    author_index, confidence = combine_events(events, candidates)
    print "combine_events"

    return (author_index, confidence)
