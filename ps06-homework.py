from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Путь к chromedriver
chromedriver_path = r"C:\Users\Денис Сорокопуд\.cache\selenium\chromedriver\win64\136.0.7103.113\chromedriver.exe"

# Настройки Chrome
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")  # Если нужно запустить в фоне

# Запуск драйвера
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    url = "https://www.divan.ru/category/kompyuternye-kresla-i-stulya"
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid^="product-card"]')))

    # Прокрутка страницы для подгрузки всех товаров
    prev_items_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        items_now = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid^="product-card"]')
        if len(items_now) == prev_items_count:
            break
        prev_items_count = len(items_now)

    # Сбор данных
    items = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid^="product-card"]')
    results = []

    for item in items:
        try:
            name_el = item.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]')
            name = name_el.text.strip()

            link_el = item.find_element(By.CSS_SELECTOR, 'a[href*="/product/"]')
            url = link_el.get_attribute("href")

            try:
                price = item.find_element(By.CSS_SELECTOR, 'span[data-testid="price"]').text.strip()
            except:
                price = "Нет цены"

            print(f"Товар: {name}, Цена: {price}, Ссылка: {url}")
            results.append({"Название": name, "Цена": price, "Ссылка": url})
        except Exception as e:
            print("Ошибка в товаре:", e)

    # Сохраняем в CSV с кодировкой utf-8-sig для правильного отображения в Excel
    with open("komp_stoly.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Название", "Цена", "Ссылка"])
        writer.writeheader()
        writer.writerows(results)

    print("✅ Данные сохранены в komp_stoly.csv")

except Exception as e:
    print("Ошибка во время выполнения:", e)

finally:
    driver.quit()









