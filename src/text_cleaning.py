import re
# ---------- 1. patterns ----------
start_pattern = re.compile(r"\*{3}\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK\b.*?\*{3}", re.IGNORECASE)
end_pattern = re.compile(r"\*{3}\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK\b.*?\*{3}",re.IGNORECASE)
heading_pattern = re.compile(r"^ *(?:CHAPTER|VOLUME) [IVXLC]+\. *$", re.MULTILINE)

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
def clean(text):
    text = cut_gutenberg(text)
    text = remove_headings(text)
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
    assert remove_headings("He read CHAPTER I.") == "He read CHAPTER I."
    assert remove_headings("CHAPTER I. was dull.") == "CHAPTER I. was dull."
    assert remove_headings(" CHAPTER IV. ") == ""
    print("tests passed")