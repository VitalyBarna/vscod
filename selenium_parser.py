from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
import os

# --- НАСТРОЙКИ ---
working_dir = '/Users/vitalijkovalenko/Downloads/VSCod'
file_path = os.path.join(working_dir, 'results.csv')
keywords = ["Zuckerberg", "Threads", "Meta", "AI"]
accounts = [
    "https://www.threads.net/@zuck",
    "https://www.threads.net/@mosseri"
]

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

all_found_data = []

try:
    for url in accounts:
        driver.get(url)
        print(f"🕵️ Изучаем профиль: {url}")
        time.sleep(5) 

        # СКРОЛЛИНГ (2 раза)
        for i in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"  📜 Прокрутка {i+1}...")
            time.sleep(4)

        # СБОР ПОСТОВ
        posts = driver.find_elements(By.CSS_SELECTOR, "span")
        for post in posts:
            try:
                # ОЧИСТКА: убираем лишние пробелы и переносы строк
                text = post.text.replace('\n', ' ').strip()
                
                if len(text) > 10:
                    for word in keywords:
                        if word.lower() in text.lower():
                            all_found_data.append({
                                "account": url,
                                "keyword": word, 
                                "content": text[:150] # Берем чуть больше текста
                            })
                            print(f"  ✨ Найдено совпадение: {word}")
                            break 
            except:
                continue

    # ЗАПИСЬ ВСЕХ ДАННЫХ
    if all_found_data:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["account", "keyword", "content"])
            writer.writeheader()
            writer.writerows(all_found_data)
        print(f"\n🏆 УСПЕХ! Данные из всех профилей сохранены в: {file_path}")

finally:
    driver.quit()
    print("🤖 Браузер закрыт.")