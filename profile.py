from collections import Counter

# Class for author profile
class Profile:
    def __init__(self, *rest_text):
        self.texts = []
        self.single_text = ""
        if rest_text:
            apply(self.add_texts, rest_text)

    # Add a single text
    def add_text(self, new_text):
        new_text = new_text.replace("\n", " ")
        self.texts.append(new_text)

        if len(self.single_text) > 0:
            self.single_text = self.single_text + " " + new_text
        else:
            self.single_text = new_text

    # Add multiple textsshell    
    def add_texts(self, *new_texts):
        for new_text in new_texts:
            self.add_text(new_text)
