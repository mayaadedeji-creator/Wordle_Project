"""
Wordle Pattern Sorter
---------------------
Groups a word list into Wordle result patterns using only plain dicts and lists.
Each pattern key is a 5-character string:
    G = Green  (right letter, right position)
    Y = Yellow (right letter, wrong position)
    B = Black  (letter not in word)

Main entry point:
    result = sort_words_by_pattern(target, word_list)
    # returns { "GYBBG": ["adore", ...], "GGGGG": ["abide"], ... }
"""

ALL_PATTERNS = [
    "GGGGG",
    "GGGGB", "GGGBG", "GGBGG", "GBGGG", "BGGGG",
    "GGGGY", "GGGYG", "GGYGG", "GYGGG", "YGGGG",
    "GGGBB", "GGBGB", "GBGGB", "BGGGB",
    "GGBBG", "GBGBG", "BGGBG",
    "GBBGG", "BGBGG", "BBGGG",
    "YYYYY",
    "BBBBY", "BBBGB",
    "BBBBB",
]

# Deduplicate while preserving order
_seen = []
for _p in ALL_PATTERNS:
    if _p not in _seen:
        _seen.append(_p)
ALL_PATTERNS = _seen


def build_empty_pattern_dict():
    """Return a fresh dict with every pre-defined pattern mapped to an empty list."""
    return {pattern: [] for pattern in ALL_PATTERNS}


def get_pattern_string(target, guess):
    """
    Compute the 5-character Wordle pattern string for a guess against a target.

    Args:
        target (str): The secret word.
        guess  (str): The guessed word (must be the same length as target).

    Returns:
        str: A 5-character string such as 'GYBBG'.
    """
    target = target.lower()
    guess  = guess.lower()
    n      = len(target)
    result = ['B'] * n
    remaining = list(target)

    for i in range(n):
        if guess[i] == target[i]:
            result[i]    = 'G'
            remaining[i] = None

    for i in range(n):
        if result[i] == 'G':
            continue
        if guess[i] in remaining:
            result[i] = 'Y'
            remaining[remaining.index(guess[i])] = None

    return ''.join(result)


def sort_words_by_pattern(target, word_list):
    """
    Sort every word in word_list into its Wordle pattern bucket.

    All 25 pre-defined pattern keys are present in the returned dict from the
    start. Any pattern that occurs but falls outside the pre-defined 25 is
    added dynamically. Empty buckets are kept so every pattern is always
    accessible. Words whose length differs from the target go into 'OTHER'.

    Args:
        target    (str):       The secret Wordle word.
        word_list (list[str]): The candidate word list to sort.

    Returns:
        dict: { pattern_string: [list of matching words] }

    Example:
        >>> sort_words_by_pattern("abide", ["adore", "abide", "funky"])
        {
            ...
            "GYBBG": ["adore"],
            "GGGGG": ["abide"],
            "BBBBB": ["funky"],
            ...
        }
    """
    groups = build_empty_pattern_dict()
    groups['OTHER'] = []
    for word in word_list:
        if len(word) != len(target):
            groups['OTHER'].append(word)
            continue

        pattern = get_pattern_string(target, word)

        if pattern not in groups:
            groups[pattern] = []

        groups[pattern].append(word)

    return groups


def load_words_from_file(filepath):
    """
    Load a word list from a file. 
    Handles multiple words per line separated by spaces.
    """
    words = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # .split() splits the line by any whitespace (spaces, tabs, newlines)
                # and returns a list of individual strings.
                line_words = line.split() 
                for word in line_words:
                    clean_word = word.strip()
                    if clean_word:
                        words.append(clean_word)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    
    return words


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    TARGET = "abide"

    WORD_LIST = load_words_from_file("Wordle_Project/wordle_dictionary_balanced.txt")

    result = sort_words_by_pattern(TARGET, WORD_LIST)

    for pattern, words in result.items():
        if words:
            print(f"{pattern}: {words}")