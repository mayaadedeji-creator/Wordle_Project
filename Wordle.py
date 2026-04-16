import random
import time
from sorting import get_pattern_string
from scoring import pick_best_guess, rank_all_guesses


def load_word_list(filename="wordle_dictionary_balanced.txt"):
    """Load and clean 5-letter words from file."""
    words = []
    try:
        with open(filename, "r") as f:
            for line in f:
                for word in line.split():
                    word = word.strip().upper()
                    if len(word) == 5:
                        words.append(word)
        # Remove duplicates while preserving order
        seen = set()
        unique_words = []
        for w in words:
            if w not in seen:
                seen.add(w)
                unique_words.append(w)
        return unique_words
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []


def filter_possible_words(possible, guess, feedback):
    """
    Keep only words that would produce the same feedback pattern
    when 'guess' is played against them (as the secret).
    """
    return [w for w in possible if get_pattern_string(w, guess) == feedback]


def display_feedback(pattern):
    """Convert G/Y/B to emoji squares."""
    emoji_map = {'G': '🟩', 'Y': '🟨', 'B': '⬛'}
    return ' '.join(emoji_map.get(ch, '?') for ch in pattern)


def main():
    print("Welcome to a Smarter Wordle!")
    time.sleep(1)
    username = input("What is your name? ").strip()
    print(f"\nHello, {username.capitalize()}! Here's how it works:")
    time.sleep(1)
    print("- You have 6 guesses to find a 5-letter word.")
    print("- After each guess, you'll see feedback:")
    print("    🟩 = correct letter, correct position")
    print("    🟨 = correct letter, wrong position")
    print("    ⬛ = letter not in the word")
    print("- The game will also suggest the best next guess")
    print("  based on probability (minimizing expected remaining words).\n")
    time.sleep(3)

    # Load the dictionary
    all_words = load_word_list()
    if not all_words:
        print("No words loaded. Exiting.")
        return
    print(f"Loaded {len(all_words)} possible words.\n")

    while True:
        secret = random.choice(all_words)
        possible = all_words.copy()   # remaining candidates
        attempts = 0
        max_attempts = 6
        guessed = False

        print("New game! Start guessing.\n")

        while attempts < max_attempts and not guessed:
            # Show hint if there are multiple possibilities
            if len(possible) > 1:
                best_guess = pick_best_guess(possible, method="expected")
                print(f"Hint: The best next guess is '{best_guess}'")
            elif len(possible) == 1:
                print(f"Hint: Only one word remains: '{possible[0]}'")

            guess = input(
                f"\nAttempt {attempts+1}/{max_attempts}: ").strip().upper()

            # Validation
            if len(guess) != 5:
                print("Please enter exactly 5 letters.")
                continue
            if guess not in all_words:
                print("Word not in dictionary. Try another word.")
                continue

            attempts += 1

            # Get feedback from the secret
            pattern = get_pattern_string(secret, guess)
            print(f"  {display_feedback(pattern)}")

            # Check win
            if guess == secret:
                print(
                    f"\nCongratulations, {username.capitalize()}! You solved it in {attempts} tries.")
                guessed = True
                break

            # Update possible words based on the feedback
            possible = filter_possible_words(possible, guess, pattern)
            if not possible:
                print("Something went wrong – no possible words left.")
                break

        if not guessed:
            print(f"\nOut of guesses! The word was {secret}.")

        # Replay
        replay = input("\nPlay again? (Y/N): ").strip().upper()
        if replay != 'Y':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
