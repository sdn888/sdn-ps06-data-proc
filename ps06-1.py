import requests
from bs4 import BeautifulSoup
url = "https://"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
rows = soup.find_all("tr")
# tr - каждый ряд таблицы
# td - каждая ячейка внутри ряда таблицы
data = []

# Теперь нам нужно перебрать коллекцию. Используем цикл “for”.

for row in rows:
    cols = row.find_all("td")
    # Используем укороченный вариант цикла for
    # Для удаления пробелов и других лишних символов используем функцию strip
    cleaned_cols = [col.text.strip() for col in cols]
    # Чтобы удалить пробелы, оставляем ()
    # Чтобы удалить какие-то символы из начала и конца, пишем ('то-что-надо-удалить')
    data.append(cleaned_cols)
    # Функция append добавляет в список.
print(data)