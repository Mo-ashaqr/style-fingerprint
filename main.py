from text_cleaning import clean, start_pattern, end_pattern, heading_pattern
from pathlib import Path
data_dir = Path('data')
files_to_open = [
                 "austen_emma.txt",
                 "austen_pride.txt",
                 "dickens_cities.txt",
                 "dickens_twist.txt"
                 ]
cleaned_books = {}
for filename in files_to_open:
    with open(data_dir / filename, mode="r", encoding="utf-8") as file:
        raw_text = file.read()
        cleaned_text = clean(raw_text)
        cleaned_books[filename] = cleaned_text
print(f"Chapter and volume = {len(heading_pattern.findall(cleaned_books["austen_emma.txt"]))}")
underscore_count = cleaned_books["austen_emma.txt"].count("_")
print(f"Underscore counts = {underscore_count}")
cleaned_heading = heading_pattern.sub("", cleaned_books["austen_emma.txt"])
# print(repr(cleaned_heading))
print(len(heading_pattern.findall(cleaned_heading)))
print(len(cleaned_books["austen_emma.txt"]) - len(cleaned_heading))


