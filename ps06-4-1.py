import time
import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)

driver = webdriver.Firefox()
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

wait = WebDriverWait(driver, 15)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-qa="vacancy-serp__vacancy"]')))

# Прокрутка страницы вниз, пока не перестанут подгружаться новые вакансии
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

vacancies = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa="vacancy-serp__vacancy"]')
logging.info(f"Найдено вакансий: {len(vacancies)}")

parsed_data = []

for vacancy in vacancies:
    try:
        title_elem = vacancy.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-serp__vacancy-title"]')
        title = title_elem.text
        link = title_elem.get_attribute('href')
    except Exception as e:
        logging.warning(f"Ошибка с названием/ссылкой: {e}")
        title = "Нет названия"
        link = "Нет ссылки"

    try:
        company = vacancy.find_element(By.CSS_SELECTOR, 'div[data-qa="vacancy-serp__vacancy-employer"]').text
    except Exception as e:
        logging.warning(f"Ошибка с компанией: {e}")
        company = "Не указана"

    try:
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-compensation"]').text
    except Exception as e:
        logging.warning(f"Ошибка с зарплатой: {e}")
        salary = "Не указана"

    parsed_data.append([title, company, salary, link])

driver.quit()

with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Компания', 'Зарплата', 'Ссылка'])
    writer.writerows(parsed_data)

logging.info("Парсинг завершён. Данные сохранены в hh.csv.")


