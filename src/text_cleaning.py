import re
# ---------- 1. patterns ----------
start_pattern = re.compile(r"\*{3}\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK\b.*?\*{3}", re.IGNORECASE)
end_pattern = re.compile(r"\*{3}\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK\b.*?\*{3}",re.IGNORECASE)
heading_pattern = re.compile(r"^[ \t]*(?:CHAPTER|VOLUME)[ \t]+[IVXLCDM]+\.?(?:[ \t]+[^\r\n]+)?[ \t]*$",re.MULTILINE | re.IGNORECASE)
end_marker = re.compile(r"^ *(?:FINIS|THE END)\.? *$", re.IGNORECASE | re.MULTILINE)
underscore_remove = re.compile(r"_([^_\n]+)_")

# ---------- 2. defs ----------
def cut_gutenberg(text):
    start = start_pattern.search(text)
    if start is None:
        raise ValueError("Start marker not found.")
    end = end_pattern.search(text, start.end())
    if end is None:
        raise ValueError("End marker not found.")
    return text[start.end():end.start()].strip()

def remove_headings(text):
    return heading_pattern.sub("", text)

def remove_end_marker(text):
    return end_marker.sub("", text)

def remove_underscores(text):
    return underscore_remove.sub(r"\1", text)

def unwrap_lines(text):
    paragraphs = re.split(r"\n\s*\n", text)
    cleaned_paragraphs = []
    for p in paragraphs:
        if p.strip():
            cleaned_paragraphs.append(" ".join(p.split()))
    return "\n\n".join(cleaned_paragraphs)

def cut_front_matter(text, anchor):
    pos = text.find(anchor)
    if pos == -1:
        raise ValueError("Anchor not found.")
    return text[pos:]

def normalize_heading(text):
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-")

    text = " ".join(text.split())

    return text.casefold().rstrip(" .;:")

def remove_descriptive_headings(text, headings):
    normalized_headings = {
        normalize_heading(title) for title in headings
    }
    paragraphs = text.split("\n\n")
    cleaned_paragraphs = []
    for paragraph in paragraphs:
        normalized_paragraph = normalize_heading(paragraph)
        if normalized_paragraph not in normalized_headings:
            cleaned_paragraphs.append(paragraph)
    return "\n\n".join(cleaned_paragraphs)

def clean(text, anchor, headings=None):

    text = cut_gutenberg(text)
    text = remove_headings(text)
    text = remove_end_marker(text)
    text = unwrap_lines(text)
    text = remove_underscores(text)
    text = cut_front_matter(text, anchor)
    if headings:
        text = remove_descriptive_headings(text, headings)

    return text.strip()

#--------------------------------------------------------

if __name__ == "__main__":
    fake = ("header\n*** START OF THE PROJECT GUTENBERG EBOOK X ***\nbody\n"
            "*** END OF THE PROJECT GUTENBERG EBOOK X ***\nfooter")

    assert cut_gutenberg(fake) == "body"
    try:
        cut_gutenberg("no markers here")
        raise AssertionError("expected a ValueError")
    except ValueError:
        pass
    assert remove_headings("CHAPTER XII.") == ""
    assert remove_headings("CHAPTER XII") == ""
    assert remove_headings("He read CHAPTER I.") == "He read CHAPTER I."
    assert remove_headings("CHAPTER I. was dull.") == "CHAPTER I. was dull."
    assert remove_headings(" CHAPTER IV. ") == ""
    assert unwrap_lines("The king walked\nin.") == "The king walked in."
    assert unwrap_lines("One.\n\nTwo.") == "One.\n\nTwo."
    assert unwrap_lines("a   b") == "a b"
    sample = "Emma\n\nby Jane Austen\n\nContents\n\nEmma Woodhouse, handsome, clever, and rich."
    result = cut_front_matter(sample, "Emma Woodhouse, handsome, clever, and rich.")
    assert result.startswith("Emma Woodhouse, handsome")
    assert "Contents" not in result
    try:
        cut_front_matter("some text", "missing anchor")
        raise AssertionError("expected a ValueError")
    except ValueError:
        pass

    print("tests passed")
