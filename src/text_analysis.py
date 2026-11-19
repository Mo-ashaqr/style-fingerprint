import re
word_pattern = re.compile(
    r"[^\W\d_]+(?:['’][^\W\d_]+)*"
)

def tokenize(text):
    text = text.casefold()
    tokens = word_pattern.findall(text)
    return tokens
