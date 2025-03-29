def process_words(file_path, length):
    words = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if len(word) == length and not word[0].isupper():
                words.append(word)
    return words

# Обробка слів на 4 та 7 букв
words_4 = process_words('words_4_letters.txt', 4)
words_7 = process_words('words_7_letters.txt', 7)

# Генерація файлу words.py
with open('words.py', 'w', encoding='utf-8') as f:
    f.write(f"fourLetterWord = {words_4}\n")
    f.write(f"sevenLetterWord = {words_7}\n")

print("Файл words.py успішно створено!")
