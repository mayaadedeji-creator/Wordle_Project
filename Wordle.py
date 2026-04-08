# Gets the 'random' and 'time' libraries
import random 
import time


# Greets user, explains the rules
print("Welcome to Wordle for Discrete Math!")
time.sleep(2)
username = input("What is your name? ")
print("Hello, " + username.capitalize() + "! The rules are simple: ")
time.sleep(2.5)
print("Choose your language.")
time.sleep(2)
print("Then, enter a FIVE-LETTER word of that language.")
time.sleep(2.5)
print("The code will let you know if letters are correct") 
print("and/or correctly placed.")
time.sleep(2.5)
print("No letters are allowed to be reused in a word.")
time.sleep(2)

# Asks user if they are ready to play
ready = input("Are you ready, " + username.capitalize() + "? Y/N (cap-sensitive): ")
while True:
    # What to do if user inputs "Y"
    if ready == "Y":
        # Asks for language
        language = input("English or Spanish? Click anything to exit. (case-sensitive) ")
    
        # What to do if user inputs "English"
        if language == "English":
            # Opens the file in read mode ('r' signifies 'read')
            with open("poss_words_english.txt", "r") as file:
                allText = file.read()
                words = list(map(str, allText.split()))
              
                # Chooses a random word as the Wordle
                wordle = random.choice(words)
        # What to do if user inputs "Spanish"
        elif language == "Spanish":
            # Opens the file in read mode ('r' signifies 'read')
            with open("poss_words_spanish.txt", "r") as file:
                allText = file.read()
                words = list(map(str, allText.split()))
                
                # Chooses a random word as the Wordle
                wordle = random.choice(words)
        # Neither of the above scenario
        else:
            print("Bye!")
            break
        
        # Defines the 'check for correct place' function
        def check_place(char_g, char_w, place):
            if char_g == char_w:
                print(place + " letter: right letter, right place!")
        
        # User's first guess
        guess = input("Enter a word: ")
        
        # Forces the user to enter ONLY a five-letter word
        while (len(guess) != 5):
            print("That was not a five letter word!")
            guess = input("Enter a word: ")
            
        # For loop repeats the guesses five more times for a total of six times
        for i in range(5):
            
            # Checks if the Wordle has been guessed
            if guess == wordle:
                print("You guessed it!")
                break
              
            # Checks correct letter guess and letter placement for place 1
            check_place(guess[0], wordle[0], "First")
            if guess[0] == wordle[1] or guess[0] == wordle [2] or guess[0] == wordle [3] or guess[0] == wordle[4]:
                print("First letter: right letter, wrong place.")
            
            # Checks correct letter guess and letter placement for place 2
            check_place(guess[1], wordle[1], "Second")
            if guess[1] == wordle[0] or guess[1] == wordle [2] or guess[1] == wordle [3] or guess[1] == wordle[4]:
                print("Second letter: right letter, wrong place.")
            
            # Checks correct letter guess and letter placement for place 3    
            check_place(guess[2], wordle[2], "Third")
            if guess[2] == wordle[0] or guess[2] == wordle [1] or guess[2] == wordle [3] or guess[2] == wordle[4]:
                print("Third letter: right letter, wrong place.")
            
            # Checks correct letter guess and letter placement for place 4
            check_place(guess[3], wordle[3], "Fourth")
            if guess[3] == wordle[0] or guess[3] == wordle [1] or guess[3] == wordle [2] or guess[3] == wordle[4]:
                print("Fourth letter: right letter, wrong place.")
            
            # Checks correct letter guess and letter placement for place 5
            check_place(guess[4], wordle[4], "Fifth")
            if guess[4] == wordle[0] or guess[4] == wordle [1] or guess[4] == wordle [2] or guess[4] == wordle[3]:
                print("Fifth letter: right letter, wrong place.")
            
            # Prompts user to keep guessing while the for loop runs
            guess = input("Enter a word: ")
            while (len(guess) != 5):
                print("That was not a five letter word!")
                guess = input("Enter a word: ")
            
        # Prints a "sorry" message if the user is unsuccessful
        if guess != wordle:
            print("You have used up your guesses. The Wordle was " + wordle + ".")
            print("Try again next time!")
            break
    # What to do if user inputs "N"
    elif ready == "N":
        print("Not ready yet? Press the Run button when you are!")
        break
    # Invalid input scenario
    else:
        print("Invalid input.")
        break

