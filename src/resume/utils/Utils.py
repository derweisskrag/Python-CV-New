import pyphen

class TextFormatter:
    @staticmethod
    def helper(lst):
        for i in range(len(lst) - 1):
            if lst[i].endswith("."):
                lst[i + 1] = lst[i + 1].capitalize()
        return lst

    @staticmethod
    def capitalize_decorator(func):
        def wrapper(text):
            capitalized_text = func(text)
            capitalize_words = {'i', 'english', 'estonian', "russian", "description:"}
            words = capitalized_text.split()
            capitalized_words = [word.capitalize() if word.replace("&shy;", "").lower() in capitalize_words else word for word in words]
            capitalized_words = TextFormatter.helper(capitalized_words)
            return ' '.join(capitalized_words)
        return wrapper

    @staticmethod
    def hyphenate_decorator(func):
        def wrapper(text):
            # Preprocess the text before hyphenation
            preprocessed_text = text.lower()
            hyphenated_text = func(preprocessed_text)
            # Postprocess the hyphenated text
            postprocessed_text = hyphenated_text.capitalize()
            return postprocessed_text
        return wrapper

    @classmethod
    def format_text(cls, text):
        hyphenator = pyphen.Pyphen(lang='en_US')  # Explicitly set language to English (US)

        lines = text.split("\n")
        words = [line.split() for line in lines]

        hyphenated_lines = []
        for line in words:
            hyphenated_words = []
            for word in line:
                hyphenated_word = hyphenator.inserted(word, '&shy;')
                hyphenated_words.append(hyphenated_word)
            hyphenated_line = ' '.join(hyphenated_words)
            hyphenated_lines.append(hyphenated_line)
        return "\n".join(hyphenated_lines)

    @classmethod
    def process_descriptions(cls, descriptions):
        result = []
        for description in descriptions:
            if not description.strip():  # Check if description is empty or contains only whitespace
                result.append(description)
            else:
                formated = cls.format_text(description)
                words_list = formated.split()
                if words_list[-1] == '.':
                    words_list = words_list[:-1]  # Remove the last element (the dummy period)
                formated = ' '.join(cls.helper(words_list))  # Apply the helper function and join the words back to a string
                result.append(formated)
        return result

    @classmethod
    def get_formatted_text(cls, text):
        formatted_text = cls.process_descriptions([text])
        return formatted_text[0]
