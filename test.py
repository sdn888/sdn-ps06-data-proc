import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = r"C:\Users\Денис Сорокопуд\.cache\selenium\chromedriver\win64\137.0.7151.68\chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)

options = Options()
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.divan.ru/category/kompyuternye-kresla-i-stulya"
driver.get(url)

time.sleep(5)

for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

html = driver.page_source
with open("page_dump.html", "w", encoding="utf-8") as f:
    f.write(html)
print("HTML страницы сохранён в page_dump.html")

# Попробуем найти все элементы с тегом 'article' — часто карточки товаров там
items = driver.find_elements(By.TAG_NAME, "article")
print(f"Найдено элементов article: {len(items)}")

if len(items) == 0:
    print("❌ Не найдено элементов article. Попробуй вручную проверить page_dump.html")
else:
    for idx, item in enumerate(items[:10], 1):
        # Попытка вывести название и цену — возможные классы
        title = ""
        price = ""
        try:
            title = item.find_element(By.CSS_SELECTOR, "[class*=name], [class*=title]").text.strip()
        except:
            title = "Нет названия"

        try:
            price = item.find_element(By.CSS_SELECTOR, "[class*=price]").text.strip()
        except:
            price = "Нет цены"

        print(f"{idx}. Товар: {title}, Цена: {price}")

driver.quit()

