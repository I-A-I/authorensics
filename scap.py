# Class for author profile
class Profile:
    def __init__(self):
        pass

    # Text will be analyzed
    def add_text(self, new_text):
        text_profile = self.analyze_text(new_text)
        self.profile = self.merge_profiles(self.profile, text_profile)

    # Add multiple texts
    def add_texts(self, new_texts*):
        for new_text in new_texts:
            self.add_text(new_texT)

    def find_distance(self, other_profile):
        pass


if __name__ == "__main__":
    pass
