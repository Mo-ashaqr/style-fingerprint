from text_cleaning import clean, start_pattern, end_pattern, heading_pattern, cut_gutenberg, remove_headings
from pathlib import Path
data_dir = Path('data')
files_to_open = [
                 "austen_emma.txt",
                 ]

anchor = "Emma Woodhouse, handsome, clever, and rich"
cleaned_books = {}
raw_books = {}
for filename in files_to_open:
    with open(data_dir / filename, mode="r", encoding="utf-8") as file:
        raw_text = file.read()
        raw_books[filename] = raw_text
        cleaned_text = clean(raw_text, anchor)
        cleaned_books[filename] = cleaned_text

emma_raw = raw_books["austen_emma.txt"]
emma_cleaned = cleaned_books["austen_emma.txt"]
body = cut_gutenberg(emma_raw)
no_headings = remove_headings(body)
print(len(emma_raw) - len(body))
print(len(body) - len(no_headings))
print(repr(emma_cleaned)[:1500])
print(" ")
print(repr(emma_cleaned)[-800:])
print(f"Chapter and volume = {len(heading_pattern.findall(cleaned_books["austen_emma.txt"]))}")
print(cleaned_books["austen_emma.txt"].lower().count("gutenberg"))
underscore_count = cleaned_books["austen_emma.txt"].count("_")
print(f"Underscore counts = {underscore_count}")
# cleaned_heading = heading_pattern.sub("", cleaned_books["austen_emma.txt"])
# print(repr(cleaned_heading))
# print(len(heading_pattern.findall(cleaned_heading)))
# print(len(cleaned_books["austen_emma.txt"]) - len(cleaned_heading))


