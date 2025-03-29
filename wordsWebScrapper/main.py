import requests
from bs4 import BeautifulSoup
import time

def get_words_from_category(category_url):
    words = []
    base_url = 'https://uk.wiktionary.org'
    next_page = category_url

    while next_page:
        response = requests.get(next_page)
        if response.status_code != 200:
            print(f"Помилка при доступі до {next_page}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        # Знаходимо всі посилання на слова в категорії
        for li in soup.select('.mw-category-group ul li'):
            word = li.a.text.strip()
            words.append(word)

        # Знаходимо посилання на наступну сторінку категорії
        next_link = soup.find('a', string='наступна сторінка')
        if next_link:
            next_page = base_url + next_link['href']
            time.sleep(1)  # Затримка між запитами, щоб не перевантажувати сервер
        else:
            next_page = None

    return words

# URL категорій
category_4_letters = 'https://uk.wiktionary.org/wiki/Категорія:Слова_з_4_букв/uk'
category_7_letters = 'https://uk.wiktionary.org/wiki/Категорія:Слова_з_7_букв/uk'

# Отримуємо слова з обох категорій
words_4_letters = get_words_from_category(category_4_letters)
words_7_letters = get_words_from_category(category_7_letters)

# Зберігаємо результати у файли
with open('words_4_letters.txt', 'w', encoding='utf-8') as f:
    for word in words_4_letters:
        f.write(word + '\n')

with open('words_7_letters.txt', 'w', encoding='utf-8') as f:
    for word in words_7_letters:
        f.write(word + '\n')

print(f"Зібрано {len(words_4_letters)} слів із 4 букв та {len(words_7_letters)} слів із 7 букв.")
