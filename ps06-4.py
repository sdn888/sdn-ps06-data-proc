import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

options = Options()
options.set_preference("general.useragent.override",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")

driver = webdriver.Firefox(options=options)
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-qa="vacancy-serp__vacancy"]')))
time.sleep(2)  # для надёжности

vacancies = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa="vacancy-serp__vacancy"]')
print(f"Найдено вакансий: {len(vacancies)}")

parsed_data = []

for vacancy in vacancies:
    # Название вакансии и ссылка
    try:
        title_element = vacancy.find_element(By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]')
        title = title_element.text.strip()
        link = title_element.get_attribute('href')
    except:
        title = "Нет названия"
        link = "Нет ссылки"

    # Компания
    try:
        company = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-employer"]').text.strip()
    except:
        company = "Не указана"

    # Зарплата
    try:
        salary = vacancy.find_element(By.CSS_SELECTOR, 'div.compensation-labels--vwum2s12fQUurc2J, span.compensation-labels--vwum2s12fQUurc2J').text.strip()
    except:
        # Попытка найти альтернативный селектор, т.к. может быть разная разметка
        try:
            salary = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-compensation"]').text.strip()
        except:
            salary = "Не указана"

    parsed_data.append([title, company, salary, link])

driver.quit()

with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Компания', 'Зарплата', 'Ссылка'])
    writer.writerows(parsed_data)

print("Парсинг завершён. Данные сохранены в hh.csv.")



