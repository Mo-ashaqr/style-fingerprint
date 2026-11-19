from pathlib import Path
from text_cleaning import clean, normalize_heading, heading_pattern
from text_analysis import tokenize
from collections import Counter
cities_headings = """
The Period
The Mail
The Night Shadows
The Preparation
The Wine-shop
The Shoemaker
Five Years Later
A Sight
A Disappointment
Congratulatory
The Jackal
Hundreds of People
Monseigneur in Town
Monseigneur in the Country
The Gorgon's Head
Two Promises
A Companion Picture
The Fellow of Delicacy
The Fellow of No Delicacy
The Honest Tradesman
Knitting
Still Knitting
One Night
Nine Days
An Opinion
A Plea
Echoing Footsteps
The Sea Still Rises
Fire Rises
Drawn to the Loadstone Rock
In Secret
The Grindstone
The Shadow
Calm in Storm
The Wood-Sawyer
Triumph
A Knock at the Door
A Hand at Cards
The Game Made
The Substance of the Shadow
Dusk
Darkness
Fifty-two
The Knitting Done
The Footsteps Die Out For Ever
""".splitlines()

cities_structural_headings = [
    "Book the First--Recalled to Life",
    "Book the Second--the Golden Thread",
    "Book the Third--the Track of a Storm",
    "The end of the first book.",
    "The end of the second book."
]
cities_headings = [
    heading.strip()
    for heading in cities_headings
    if heading.strip()
]


cities_headings.extend(cities_structural_headings)
twist_headings = """
TREATS OF THE PLACE WHERE OLIVER TWIST WAS BORN AND OF THE CIRCUMSTANCES ATTENDING HIS BIRTH
TREATS OF OLIVER TWIST'S GROWTH, EDUCATION, AND BOARD
RELATES HOW OLIVER TWIST WAS VERY NEAR GETTING A PLACE WHICH WOULD NOT HAVE BEEN A SINECURE
OLIVER, BEING OFFERED ANOTHER PLACE, MAKES HIS FIRST ENTRY INTO PUBLIC LIFE
OLIVER MINGLES WITH NEW ASSOCIATES. GOING TO A FUNERAL FOR THE FIRST TIME, HE FORMS AN UNFAVOURABLE NOTION OF HIS MASTER'S BUSINESS
OLIVER, BEING GOADED BY THE TAUNTS OF NOAH, ROUSES INTO ACTION, AND RATHER ASTONISHES HIM
OLIVER CONTINUES REFRACTORY
OLIVER WALKS TO LONDON. HE ENCOUNTERS ON THE ROAD A STRANGE SORT OF YOUNG GENTLEMAN
CONTAINING FURTHER PARTICULARS CONCERNING THE PLEASANT OLD GENTLEMAN, AND HIS HOPEFUL PUPILS
OLIVER BECOMES BETTER ACQUAINTED WITH THE CHARACTERS OF HIS NEW ASSOCIATES; AND PURCHASES EXPERIENCE AT A HIGH PRICE. BEING A SHORT, BUT VERY IMPORTANT CHAPTER, IN THIS HISTORY
TREATS OF MR. FANG THE POLICE MAGISTRATE; AND FURNISHES A SLIGHT SPECIMEN OF HIS MODE OF ADMINISTERING JUSTICE
IN WHICH OLIVER IS TAKEN BETTER CARE OF THAN HE EVER WAS BEFORE. AND IN WHICH THE NARRATIVE REVERTS TO THE MERRY OLD GENTLEMAN AND HIS YOUTHFUL FRIENDS.
SOME NEW ACQUAINTANCES ARE INTRODUCED TO THE INTELLIGENT READER, CONNECTED WITH WHOM VARIOUS PLEASANT MATTERS ARE RELATED, APPERTAINING TO THIS HISTORY
COMPRISING FURTHER PARTICULARS OF OLIVER'S STAY AT MR. BROWNLOW'S, WITH THE REMARKABLE PREDICTION WHICH ONE MR. GRIMWIG UTTERED CONCERNING HIM, WHEN HE WENT OUT ON AN ERRAND
SHOWING HOW VERY FOND OF OLIVER TWIST, THE MERRY OLD JEW AND MISS NANCY WERE
RELATES WHAT BECAME OF OLIVER TWIST, AFTER HE HAD BEEN CLAIMED BY NANCY
OLIVER'S DESTINY CONTINUING UNPROPITIOUS, BRINGS A GREAT MAN TO LONDON TO INJURE HIS REPUTATION
HOW OLIVER PASSED HIS TIME IN THE IMPROVING SOCIETY OF HIS REPUTABLE FRIENDS
IN WHICH A NOTABLE PLAN IS DISCUSSED AND DETERMINED ON
WHEREIN OLIVER IS DELIVERED OVER TO MR. WILLIAM SIKES
THE EXPEDITION
THE BURGLARY
WHICH CONTAINS THE SUBSTANCE OF A PLEASANT CONVERSATION BETWEEN MR. BUMBLE AND A LADY; AND SHOWS THAT EVEN A BEADLE MAY BE SUSCEPTIBLE ON SOME POINTS
TREATS ON A VERY POOR SUBJECT. BUT IS A SHORT ONE, AND MAY BE FOUND OF IMPORTANCE IN THIS HISTORY
WHEREIN THIS HISTORY REVERTS TO MR. FAGIN AND COMPANY
IN WHICH A MYSTERIOUS CHARACTER APPEARS UPON THE SCENE; AND MANY THINGS, INSEPARABLE FROM THIS HISTORY, ARE DONE AND PERFORMED
ATONES FOR THE UNPOLITENESS OF A FORMER CHAPTER; WHICH DESERTED A LADY, MOST UNCEREMONIOUSLY
LOOKS AFTER OLIVER, AND PROCEEDS WITH HIS ADVENTURES
HAS AN INTRODUCTORY ACCOUNT OF THE INMATES OF THE HOUSE, TO WHICH OLIVER RESORTED
RELATES WHAT OLIVER'S NEW VISITORS THOUGHT OF HIM
INVOLVES A CRITICAL POSITION
OF THE HAPPY LIFE OLIVER BEGAN TO LEAD WITH HIS KIND FRIENDS
WHEREIN THE HAPPINESS OF OLIVER AND HIS FRIENDS, EXPERIENCES A SUDDEN CHECK
CONTAINS SOME INTRODUCTORY PARTICULARS RELATIVE TO A YOUNG GENTLEMAN WHO NOW ARRIVES UPON THE SCENE; AND A NEW ADVENTURE WHICH HAPPENED TO OLIVER
CONTAINING THE UNSATISFACTORY RESULT OF OLIVER'S ADVENTURE; AND A CONVERSATION OF SOME IMPORTANCE BETWEEN HARRY MAYLIE AND ROSE
IS A VERY SHORT ONE, AND MAY APPEAR OF NO GREAT IMPORTANCE IN ITS PLACE, BUT IT SHOULD BE READ NOTWITHSTANDING, AS A SEQUEL TO THE LAST, AND A KEY TO ONE THAT WILL FOLLOW WHEN ITS TIME ARRIVES
IN WHICH THE READER MAY PERCEIVE A CONTRAST, NOT UNCOMMON IN MATRIMONIAL CASES
CONTAINING AN ACCOUNT OF WHAT PASSED BETWEEN MR. AND MRS. BUMBLE, AND MR. MONKS, AT THEIR NOCTURNAL INTERVIEW
INTRODUCES SOME RESPECTABLE CHARACTERS WITH WHOM THE READER IS ALREADY ACQUAINTED, AND SHOWS HOW MONKS AND THE JEW LAID THEIR WORTHY HEADS TOGETHER
A STRANGE INTERVIEW, WHICH IS A SEQUEL TO THE LAST CHAMBER
CONTAINING FRESH DISCOVERIES, AND SHOWING THAT SUPRISES, LIKE MISFORTUNES, SELDOM COME ALONE
AN OLD ACQUAINTANCE OF OLIVER'S, EXHIBITING DECIDED MARKS OF GENIUS, BECOMES A PUBLIC CHARACTER IN THE METROPOLIS
WHEREIN IS SHOWN HOW THE ARTFUL DODGER GOT INTO TROUBLE
THE TIME ARRIVES FOR NANCY TO REDEEM HER PLEDGE TO ROSE MAYLIE. SHE FAILS.
NOAH CLAYPOLE IS EMPLOYED BY FAGIN ON A SECRET MISSION
THE APPOINTMENT KEPT
FATAL CONSEQUENCES
THE FLIGHT OF SIKES
MONKS AND MR. BROWNLOW AT LENGTH MEET. THEIR CONVERSATION, AND THE INTELLIGENCE THAT INTERRUPTS IT
THE PURSUIT AND ESCAPE
AFFORDING AN EXPLANATION OF MORE MYSTERIES THAN ONE, AND COMPREHENDING A PROPOSAL OF MARRIAGE WITH NO WORD OF SETTLEMENT OR PIN-MONEY
FAGIN'S LAST NIGHT ALIVE
AND LAST
""".splitlines()

twist_headings = [
    heading.strip()
    for heading in twist_headings
    if heading.strip()
]

def main():

    global type_number
    data_dir = Path("data")

    files_to_open = [
        "austen_emma.txt",
        "austen_pride.txt",
        "dickens_cities.txt",
        "dickens_twist.txt"
    ]

    anchor = {
        "austen_emma.txt": "Emma Woodhouse, handsome, clever, and rich",

        "austen_pride.txt": "It is a truth universally acknowledged",

        "dickens_cities.txt":
            "It was the best of times, it was the worst of times",

        "dickens_twist.txt":
            "Among other public buildings in a certain town"
    }

    descriptive_headings = {
        "dickens_cities.txt": cities_headings,
        "dickens_twist.txt": twist_headings
    }

    cleaned_books = {}

    tokens_by_book = {}

    for filename in files_to_open:

        with open(data_dir / filename, encoding="utf-8") as file:

            raw_text = file.read()

            book_anchor = anchor[filename]

            if book_anchor not in raw_text:
                raise ValueError(f"Anchor not found: {filename}")

            book_headings = descriptive_headings.get(filename, [])

            cleaned_text = clean(
                raw_text,
                book_anchor,
                book_headings
            )
            cleaned_books[filename] = cleaned_text

    for filename, text in cleaned_books.items():
        tokens = tokenize(text)
        tokens_by_book[filename] = tokens

    comparison_words = [
        "the", "and", "of", "to",
        "in", "it", "that", "was",
        "i", "you", "he", "she",
        "her", "his", "but", "not"
    ]
    relative_frequencies = {}

    for filename, tokens in tokens_by_book.items():
        word_counter = Counter(tokens)
        tokens_number = len(tokens)
        type_number = len(word_counter)
        print(f"\nBook: {filename}")
        # print(f"TTR = {type_number / tokens_number:.2%}")
        # print(word_counter.most_common(20))
        for word in comparison_words:
            count = word_counter[word]
            relative_frequency = (count / tokens_number) * 10000
            print(f"{word}: {relative_frequency:.2f}")

if __name__ == "__main__":
    main()