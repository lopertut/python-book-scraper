from bs4 import BeautifulSoup
import requests
import json
from dict2xml import dict2xml

page = requests.get("https://books.toscrape.com/catalogue/page-1.html")
soup = BeautifulSoup(page.content, 'html.parser')
book_cards = soup.find_all("article", class_="product_pod")

page_number = int(input("Enter the page number(max 50): "))
if page_number > 50 or page_number < 0:
    raise ValueError("Page number must be between 1 and 50")

books = {}
json_books = {
    "five-stars": [],
    "four-stars": [],
    "three-stars": [],
    "two-stars": [],
    "one-stars": []
}
xml_books = {}
index = 1

for i in range(page_number):
    for card in book_cards:
        book = {}
        # TODO: может стоит добавить заходить на страницу книги и уже оттуда брать данные

        h3_tag = card.find("h3")
        a_tag = h3_tag.find("a")
        book['title'] = a_tag['title']

        rating = card.find("p")['class'][1]
        book['rating'] = rating

        price = card.find("p", class_="price_color").text.replace("£", "")
        book['price'] = price

        in_stock = card.find("p", class_="instock availability").text.strip()
        book['stock'] = in_stock

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

        books[index] = book
        index += 1
    page = requests.get(f"https://books.toscrape.com/catalogue/page-{i}.html")

# TODO: тут надо какую то структуру сделать особеную или для xml тоже
with open('books.json', 'w') as file:
    books_json = json.dumps(json_books, indent=4)
    file.write(books_json)
    file.close()

with open('books.xml', 'w') as file:
    xml = dict2xml(books, wrap="root")
    file.write(xml)
    file.close()
