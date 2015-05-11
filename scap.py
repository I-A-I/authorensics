# This is the Source Code Authorship Profile (SCAP) method
# Based primarily on "Identifying Authorship by Byte-Level N-Grams:The Source Code Author Profile (SCAP) Method"
# Publicly available at https://www.utica.edu/academic/institutes/ecii/publications/articles/B41158D1-C829-0387-009D214D2170C321.pdf

# The range of n-grams to use for profiling
N_GRAM_MIN = 2
N_GRAM_MAX = 6

# Class for author profile
class Profile:
    def __init__(self, name=""):
        self.name = name

    # Add a single text
    def add_text(self, new_text):
        text_profile = self.analyze_text(new_text)
        self.profile = self.merge_profiles(self.profile, text_profile)

    # For every n-gram between N_GRAM_MIN and N_GRAM_MAX:
        # ... Count n-grams
        # ... Sort descendingly
        # ... Discard frequency to save memory (?)
    # Return array of arrays
    def analyze_text(self, new_text):
        pass

    # Add multiple texts
    def add_texts(self, new_texts*):
        for new_text in new_texts:
            self.add_text(new_texT)

    def merge_profiles(self, profile1, profile2):
        pass

    # For each n-gram, use the shorter profile for comparison
    # Similarity should probably be an _absolute_ measure of intersection
    # Not a proportion
    def find_distance(self, other_profile):
        pass


if __name__ == "__main__":
    pass
