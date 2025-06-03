data = [
    ['100', '200', '300'],
    ['400', '500', '600']
    ]
    # С сайта мы получаем именно списки.
numbers = []

for row in data:
    for text in row:
        number = int(text)
        numbers.append(number)
print(numbers)