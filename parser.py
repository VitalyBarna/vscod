import requests
from bs4 import BeautifulSoup

url = "https://www.threads.net/@zuck" 
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Связь установлена! ✅")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Печатаем заголовок, чтобы убедиться, что мы на нужной странице
    if soup.title:
        print("Заголовок страницы:", soup.title.text)

    # ПОИСК КЛЮЧЕВОГО СЛОВА
    keyword = "Zuckerberg"
    if keyword.lower() in response.text.lower():
        print(f"Ура! Ключевое слово '{keyword}' найдено! 🎉")
    else:
        print(f"Слово '{keyword}' не найдено в коде страницы. 🧐")

    # Сохраняем результат в файл для проверки
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(response.text)
else:
    print(f"Ошибка доступа: {response.status_code} ❌")