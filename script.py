from bs4 import BeautifulSoup
import requests
import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

page = requests.get("https://books.toscrape.com/catalogue/page-1.html")
soup = BeautifulSoup(page.content, 'html.parser')
book_cards = soup.find_all("article", class_="product_pod")

page_number = int(input("Enter the page number(max 50): "))
if page_number > 50 or page_number < 0:
    raise ValueError("Page number must be between 1 and 50")

json_books = {
    "five-stars": [],
    "four-stars": [],
    "three-stars": [],
    "two-stars": [],
    "one-stars": []
}

xml_books = {
    "in stock": [],
    "out of stock": []
}

for i in range(page_number + 1):
    for card in book_cards:
        book = {}

        # Тут мы извлекаем данные
        h3_tag = card.find("h3")
        a_tag = h3_tag.find("a")
        book['title'] = a_tag['title']

        rating = card.find("p")['class'][1]
        book['rating'] = rating

        price = card.find("p", class_="price_color").text.replace("£", "")
        book['price'] = price

        in_stock = card.find("p", class_="instock availability").text.strip()
        book['stock'] = in_stock

        # Сортируем книги по рейтингу для json файла
        if book["rating"] == "Five":
            json_books["five-stars"].append(book)
        elif book["rating"] == "Four":
            json_books["four-stars"].append(book)
        elif book["rating"] == "Three":
            json_books["three-stars"].append(book)
        elif book["rating"] == "Two":
            json_books["two-stars"].append(book)
        elif book["rating"] == "One":
            json_books["one-stars"].append(book)

        # Сортируем книги по наличию на скаладе
        if book["stock"] == "In stock":
            xml_books["in stock"].append(book)
        else:
            xml_books["out of stock"].append(book)

    page = requests.get(f"https://books.toscrape.com/catalogue/page-{i}.html")  # идем на следующию страницу каталога

# Записываем данные в json файл
with open('books.json', 'w') as file:
    books_json = json.dumps(json_books, indent=4)
    file.write(books_json)
    file.close()

# Записываем данные в xml файл
with open('books.xml', 'w') as file:
    my_item_func = lambda x: 'book'
    xml = dicttoxml(xml_books, custom_root="books", attr_type=False, item_func=my_item_func)
    file.write(parseString(xml).toprettyxml())
    file.close()
