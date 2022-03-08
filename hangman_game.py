from itertools import cycle

old_letters_guessed = []
num_of_tries = 1


def choose_word():
    """Asks the user for a file path for the words file, then asks for an index
    to choose a word from within the file.
    :return: chosen word from the file
    :rtype: str
    """

    while True:
        file_path = input("Please enter the path for your words file: ")
        try:
            opening_file_trial = open(file_path, "r")  # validation of file
            opening_file_trial.close()
            break
        except FileNotFoundError:
            print("Your file was not found, please try again.\n")
            continue

    while True:
        try:
            index = int(input("Enter index: "))  # validation of integer
            break
        except:
            print("\nInvalid input.\nPlease enter a whole number.")
            continue

    with open(file_path, "r") as words_file:
        content = words_file.read()
        words_file_list = content.split(" ")
        words_list = []
        for word in words_file_list:
            if word not in words_list:
                words_list.append(word)
        num_of_words = len(words_list)

    word_count = 0
    for word in cycle(words_file_list):  # looping the list if user index bigger than list's length
        word_count += 1
        if word_count == index:
            index_word = word
            break

    print(f"\nYour words file has {num_of_words} words.", "\nLet's start!")
    print(f"The word you chose has {len(index_word)} letters.")
    return index_word


def check_valid_input(letter_guessed):
    """Recieves a string from 'try_update_letter_guessed' and returns
    True if input is valid.
    :param letter_guessed: letter guessed from the user
    :type letter_guessed: str
    :return: True if letter_guessed valid
    :rtype: bool
    """

    letter_guessed = letter_guessed.lower()

    con1 = len(letter_guessed) == 1
    con2 = letter_guessed.isalpha()
    con3 = letter_guessed not in old_letters_guessed
    all_conditions = con1 and con2 and con3

    return all_conditions


def show_hidden_word(secret_word, old_letters_guessed):
    """Prints the secret word's letters in underscores. If any of the secret word's letters
    are in old_letters_guessed list, prints the letter instead of underscore.
    :param secret_word: the user's chosen word
    :param old_letters_guessed: list of letters already guessed by the user
    :type secret_word: str
    :type old_letters_guessed: list
    :return: underscored user's word
    :rtype: str
    """

    my_list = []
    for letter in secret_word:
        if letter in old_letters_guessed:
            my_list.append(letter)
        else:
            my_list.append("_")
    print("\n")
    print(" ".join(my_list))
    print("\n")


def try_update_letter_guessed(user_word):
    """Asks the user to input a letter, checks if the letter is valid using 'check_valid_input'.
    scenario letter valid:
    if letter in the user's word, using 'show_hidden_word' to show
    the letter in the word, adds letter to old_letters_guessed list and
    returns old_letters_guessed.
    if letter not in the user's word, adds letter to old_letters_guessed, increments num_of_tries
    by 1, shows hangman picture with 'print_hangman' and returns num_of_tries and old_letters_guessed.
    scenario letter not valid:
    prints an 'X' and the letters already guessed seperated by '->'. returns none.
    :param user_word: the user's chosen word
    :type user_word: str
    :return: updated letters guessed list, number of tries if user guessed worng. if letter
    not valid returns none.
    :rtype: old_letters_guessed: list. num_of_tries: int.
    """

    global num_of_tries

    letter_guessed = input("Guess a letter: ").lower()
    if check_valid_input(letter_guessed):

        if letter_guessed in user_word:
            old_letters_guessed.append(letter_guessed)
            show_hidden_word(user_word, old_letters_guessed)
            return old_letters_guessed
        else:
            if letter_guessed not in old_letters_guessed:
                old_letters_guessed.append(letter_guessed)
            num_of_tries += 1
            print("\n:(")
            print_hangman(num_of_tries)
            return num_of_tries, old_letters_guessed

    else:
        if len(old_letters_guessed) > 0:
            print("X")
            print(" -> ".join(sorted(old_letters_guessed)))
        else:
            print("X")


def opening_screen():
    """Prints welcoming screen and the hangman's first picture.
    :return: none
    """

    HANGMAN_ASCII_ART = ("""\nWelcome to the game HANGMAN
     _    _                                         
    | |  | |                                        
    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
    |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
    |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                            __/ |                      
                        |___/
    """)

    MAX_TRIES = 6

    print(HANGMAN_ASCII_ART)
    print(f"\nYou have {MAX_TRIES} guesses. \n")

    print_hangman(num_of_tries)

    print("\n")


def print_hangman(num_of_tries):
    """Print hangman's picture based on number recieved.
    :param num_of_tries: number of user's failed guesses
    :type num_of_tries: int
    :return: none
    """

    HANGMAN_PHOTOS = {1: "    x-------x",  # all 7 of hangman pictures
                      2: """        x-------x
        |
        |
        |
        |
        |
        """, 3: """        x-------x
        |       |
        |       0
        |
        |
        |
        """, 4: """        x-------x
        |       |
        |       0
        |       |
        |
        |
        """, 5: """        x-------x
        |       |
        |       0
        |      /|\\
        |
        |
        """, 6: """        x-------x
        |       |
        |       0
        |      /|\\
        |      /
        |
        """, 7: """        x-------x
        |       |
        |       0
        |      /|\\
        |      / \\
        |
        """}
    print(HANGMAN_PHOTOS[num_of_tries])


def check_win(user_word, old_letters_guessed):
    """Check if user got all letters of the word.
    :param user_word: the user's chosen word
    :param old_letters_guessed: list of letters already guessed by the user
    :type user_word: str
    :type old_letters_guessed: list
    :return: True if user won the game
    :rtype: bool
    """
    true = 0
    for letter in user_word:
        if letter not in old_letters_guessed:
            true += 1
    win = true == 0
    return win


def main():
    opening_screen()
    user_word = choose_word()
    show_hidden_word(user_word, old_letters_guessed)

    while True:
        if num_of_tries == 6:
            print("\nLast chance!\n")
            try_update_letter_guessed(user_word)
        elif num_of_tries == 7:
            print(f"\nYou guessed {num_of_tries - 1} times.")
            print("\nYou LOSE\n")
            break
        else:
            try_update_letter_guessed(user_word)

        if check_win(user_word, old_letters_guessed):
            print(f"You found the word: {user_word.capitalize()}")
            print("\nYou WIN\n")
            break
        else:
            continue


if __name__ == "__main__":
    main()