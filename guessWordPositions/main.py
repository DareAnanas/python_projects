def guessWordPositions(word, guess):
    if guess == word:
        return -1
    
    correct_positions = 0
    for i in range(len(word)):
        if i < len(guess) and word[i] == guess[i]:
            correct_positions += 1
    
    return correct_positions

word = "pizza"

print(guess_word(word, "aaaaa"))  # Output: 1
print(guess_word(word, "piaaz"))  # Output: 2
print(guess_word(word, "bbbbb"))  # Output: 0
print(guess_word(word, "pizza"))  # Output: -1
