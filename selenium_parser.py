from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
import os

# 1. Указываем путь к папке
working_dir = '/Users/vitalijkovalenko/Downloads/VSCod'
file_path = os.path.join(working_dir, 'results.csv')

# Настройка браузера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    url = "https://www.threads.net/@zuck"
    driver.get(url)
    print(f"📍 Работаем в папке: {working_dir}")
    print("⏳ Загружаем посты...")
    time.sleep(5) 

    # Находим элементы
    posts = driver.find_elements(By.CSS_SELECTOR, "span") 
    found_data = []
    keywords = ["Zuckerberg", "Threads", "Meta", "AI"]

    print(f"🔍 Начинаем анализ ({len(posts)} элементов)...")

    for post in posts:
        try:
            text = post.text
            if text:
                for word in keywords:
                    if word.lower() in text.lower() and len(text) > 10:
                        found_data.append({"keyword": word, "content": text[:100].strip() + "..."})
                        print(f"✨ Найдено: {word}")
                        break 
        except Exception:
            continue

    # 2. ЗАПИСЬ В ФАЙЛ (теперь строго внутри блока try с правильным отступом)
    if found_data:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["keyword", "content"])
            writer.writeheader()
            writer.writerows(found_data)
        print(f"✅ Готово! Файл создан: {file_path}")
    else:
        print("xml Совпадений не найдено, файл не создан.")

finally:
    # 3. Закрываем браузер в любом случае
    driver.quit()
    print("🤖 Браузер закрыт.")