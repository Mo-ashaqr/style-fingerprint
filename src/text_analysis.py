import re
word_pattern = re.compile(
    r"[^\W\d_]+(?:['’][^\W\d_]+)*"
)

def tokenize(text):
    text = text.casefold()
    tokens = word_pattern.findall(text)
    return tokens

def character_ngram_counts(text, n=3):
    if n <= 0:
        raise ValueError('n must be greater than zero.')
    normalized_text = " ".join(text.casefold().split())
    n_gram = [
        normalized_text[i:i + n]
        for i in range()
    ]