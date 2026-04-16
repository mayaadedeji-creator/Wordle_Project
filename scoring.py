from sorting import get_pattern_string


def partition_by_pattern(guess, word_list):
    """Group possible secret words by the feedback pattern they produce."""
    groups = {}
    for secret in word_list:
        if len(secret) != len(guess):
            continue
        pattern = get_pattern_string(secret, guess)
        groups.setdefault(pattern, []).append(secret)
    return groups


def expected_group_size(guess, word_list):
    partitions = partition_by_pattern(guess, word_list)
    total = len(word_list)
    score = sum((len(g) / total) * len(g) for g in partitions.values())
    return score


def worst_case_group_size(guess, word_list):
    partitions = partition_by_pattern(guess, word_list)
    return max((len(g) for g in partitions.values()), default=0)


def rank_all_guesses(word_list, method="expected"):
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
    if len(word_list) <= 2:
        return word_list[0]
    return rank_all_guesses(word_list, method)[0][0]


def simulate_one_game(target, full_word_list, method="expected"):
    remaining = full_word_list[:]
    for round_number in range(1, 7):
        guess = pick_best_guess(remaining, method)
        if guess == target:
            return round_number
        feedback = get_pattern_string(target, guess)
        partitions = partition_by_pattern(guess, remaining)
        remaining = partitions.get(feedback, [])
    return 7


def simulate_all_games(word_list, method="expected"):
    results = {}
    for i, target in enumerate(word_list):
        results[target] = simulate_one_game(target, word_list, method)
        if (i + 1) % 100 == 0:
            print(f"  Completed {i + 1} of {len(word_list)} games")
    return results


def print_summary(results):
    counts = list(results.values())
    avg = sum(counts) / len(counts)
    print(f"Average guesses: {avg:.2f}")
    print(f"Worst case: {max(counts)} guesses")
    wins = sum(1 for c in counts if c <= 6)
    print(f"Solved in ≤6: {wins} / {len(counts)}")
    for n in range(1, 8):
        cnt = sum(1 for c in counts if c == n)
        print(f"  {n}: {cnt} games  {'#' * cnt}")