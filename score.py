# Scoring Engine and Simulation
#
# Uses Lark's two functions:
#   get_feedback(guess, target) - returns a pattern like ("G","Y","X","X","G") that matches the target
#   get_matching_words(guess, word_list) - returns a dictionary mapping each
#       feedback pattern to the list of words that produce that pattern.
#       Every single word in the word list ends up in exactly one group.
#       The only patterns that do not appear as keys are patterns that zero words produce.


from . import get_feedback, get_matching_words



def expected_group_size(guess, word_list):
    """
    For a given guess, compute the average number of remaining words
    you would be left with after seeing the feedback.

    This is calculated as the sum of (size / total) * size for each group,
    which equals (1 / total) * sum of size squared. This is the expected
    value formula from probability: E[X] = sum of x * P(X = x).

    Lower is better. A perfect guess that uniquely identifies every word
    would score 1.0.

    Args:
        guess: a 5-letter word string to evaluate as a potential guess
        word_list: list of remaining possible answer words

    Returns:
        float: the expected number of remaining words after guessing this word
    """
    partitions = get_matching_words(guess, word_list)
    total = len(word_list)
    score = 0
    for group in partitions.values():
        size = len(group)
        score += (size / total) * size
    return score


def worst_case_group_size(guess, word_list):
    """
    For a given guess, find the largest group it could leave you with.
    This is the minimax approach: it minimizes the worst possible outcome.

    Lower is better. A perfect guess that uniquely identifies every word
    would score 1.

    Args:
        guess: a 5-letter word string to evaluate as a potential guess
        word_list: list of remaining possible answer words

    Returns:
        int: the size of the largest group produced by this guess
    """
    partitions = get_matching_words(guess, word_list)
    return max(len(group) for group in partitions.values())



def rank_all_guesses(word_list, method="expected"):
    """
    Try every word in the word list as a possible guess, score each one 
    (ie calculate the average number of remaining words that guess would 
    leave you with across all possible targets),
    and sort from best (lowest) to worst. This answers the question: out of all
    the words I could guess right now, which one would narrow things
    down the most?

    Args:
        word_list: list of remaining possible answer words. Each word
                   is tried as a potential guess and scored against
                   the full list.
        method: "expected" to rank by expected group size (best on average),
                or "worst" to rank by worst case group size (safest guarantee)

    Returns:
        list of (word, score) tuples sorted from best (lowest score) to worst
    """
    scores = []
    for guess in word_list:
        if method == "expected":
            score = expected_group_size(guess, word_list)
        else:
            score = worst_case_group_size(guess, word_list)
        scores.append((guess, score))
    scores.sort(key=lambda x: x[1])
    return scores


def pick_best_guess(word_list, method="expected"):
    """
    Return the single best word to guess next. If there are only 1 or 2
    words left, just guess the first one since there is nothing to
    optimize at that point.

    Args:
        word_list: list of remaining possible answer words
        method: "expected" or "worst", passed to rank_all_guesses

    Returns:
        str: the best word to guess next
    """
    if len(word_list) <= 2:
        return word_list[0]
    ranked = rank_all_guesses(word_list, method)
    return ranked[0][0]


def simulate_one_game(target, full_word_list, method="expected"):
    """
    Play a full Wordle game against a known target word using our
    strategy. Each round, we pick the best guess according to our
    scoring method, get the feedback, and filter down the remaining
    words. We repeat until we guess correctly or run out of 6 tries.

    Args:
        target: the hidden answer word we are trying to guess
        full_word_list: the complete list of possible answer words
        method: "expected" or "worst", passed to pick_best_guess

    Returns:
        int: the number of guesses it took to find the target,
             or 7 if we failed to solve in 6 guesses
    """
    remaining = full_word_list[:] # clone

    for round_number in range(1, 7): # 6 tries
        # out of all remaining words, pick the one that would leave the fewest remaining words on average
        guess = pick_best_guess(remaining, method)

        if guess == target:
            return round_number

        feedback = get_feedback(guess, target)

        partitions = get_matching_words(guess, remaining)
        remaining = partitions.get(feedback, [])

    return 7


def simulate_all_games(word_list, method="expected"):
    """
    Test our strategy by playing it against every possible target word
    in the word list. This tells us how the strategy performs overall:
    average guesses needed, worst case, and whether it always wins
    within 6 tries.

    Args:
        word_list: the complete list of possible answer words. Each word
                   takes a turn being the hidden target.
        method: "expected" or "worst", passed to simulate_one_game

    Returns:
        dict: mapping each target word to the number of guesses needed
              to solve it (7 means it was not solved in 6 guesses)
    """
    results = {}
    for i, target in enumerate(word_list):
        num_guesses = simulate_one_game(target, word_list, method)
        results[target] = num_guesses
        if (i + 1) % 100 == 0:
            print(f"  Completed {i + 1} of {len(word_list)} games")
    return results


def print_summary(results):
    """
    Print a summary of the simulation results including the average
    number of guesses, the worst case, the number of games solved
    in 6 or fewer guesses, and a histogram showing how many games
    were solved in each number of guesses.

    Args:
        results: dict mapping each target word to the number of
                 guesses needed, as returned by simulate_all_games
    """
    counts = list(results.values())
    average = sum(counts) / len(counts)
    worst = max(counts)
    wins = sum(1 for c in counts if c <= 6)

    print(f"Average guesses needed: {average:.2f}")
    print(f"Worst case: {worst} guesses")
    print(f"Solved in 6 or fewer: {wins} out of {len(counts)}")
    print()
    for n in range(1, 8):
        count = sum(1 for c in counts if c == n)
        bar = "#" * count
        print(f"  {n} guesses: {count} games  {bar}")


if __name__ == "__main__":

    # Load the word list
    with open("wordle_dictionary_balanced.txt") as f:
        words = [line.strip().upper() for line in f]

    # Find and display the best opening words
    print("Ranking all opening guesses...")
    print("(This may take a few minutes)\n")
    ranked = rank_all_guesses(words, method="expected")

    print("Top 10 opening words:")
    for word, score in ranked[:10]:
        print(f"  {word}  ->  expected group size: {score:.2f}")

    print()
    print("Worst 10 opening words:")
    for word, score in ranked[-10:]:
        print(f"  {word}  ->  expected group size: {score:.2f}")

    # Simulate every game
    # NOTE: This will take a long time because for each of the 2309 games
    # it has to score all remaining words at each round. You can test with
    # a smaller word list first.
    print()
    print("Running full simulation...")
    results = simulate_all_games(words, method="expected")
    print()
    print_summary(results)
