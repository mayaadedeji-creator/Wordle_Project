import random
import time

# Greets user, explains the rules
print("Welcome to Wordle for Discrete Math!")
time.sleep(2)

username = input("What is your name? ")
print("Hello, " + username.capitalize() + "! The rules are simple: ")
time.sleep(2.5)

print("Enter a FIVE-LETTER word.")
time.sleep(2.5)

print("The code will let you know if letters are correct")
print("and/or correctly placed.")
time.sleep(2.5)

print("No letters are allowed to be reused in a word.")
time.sleep(2)

# Ask if ready
ready = input("Are you ready, " + username.capitalize() + "? Y/N (cap-sensitive): ")

while True:

    if ready == "Y":

        # Load word list from file
        with open("wordle_dictionary_balanced.txt", "r") as file:
            allText = file.read()
            words = list(map(str, allText.split()))

        # Pick random word
        wordle = random.choice(words)

        # Function to check correct placement
        def check_place(char_g, char_w, place):
            if char_g == char_w:
                print(place + " letter: right letter, right place!")

        # First guess
        guess = input("Enter a word: ")

        # Ensure 5-letter word
        while len(guess) != 5:
            print("That was not a five-letter word!")
            guess = input("Enter a word: ")

        # 6 total attempts (Wordle-style)
        for i in range(5):

            if guess == wordle:
                print("You guessed it!")
                break

            # Check each position

            check_place(guess[0], wordle[0], "First")
            if guess[0] in wordle[1:]:
                print("First letter: right letter, wrong place.")

            check_place(guess[1], wordle[1], "Second")
            if guess[1] in wordle[0] + wordle[2:]:
                print("Second letter: right letter, wrong place.")

            check_place(guess[2], wordle[2], "Third")
            if guess[2] in wordle[:2] + wordle[3:]:
                print("Third letter: right letter, wrong place.")

            check_place(guess[3], wordle[3], "Fourth")
            if guess[3] in wordle[:3] + wordle[4]:
                print("Fourth letter: right letter, wrong place.")

            check_place(guess[4], wordle[4], "Fifth")
            if guess[4] in wordle[:4]:
                print("Fifth letter: right letter, wrong place.")

            # Next guess
            guess = input("Enter a word: ")

            while len(guess) != 5:
                print("That was not a five-letter word!")
                guess = input("Enter a word: ")

        # Loss message
        if guess != wordle:
            print("You have used up your guesses. The Wordle was " + wordle + ".")
            print("Try again next time!")

        break

    elif ready == "N":
        print("Not ready yet? Press the Run button when you are!")
        break

    else:
        print("Invalid input.")
        break