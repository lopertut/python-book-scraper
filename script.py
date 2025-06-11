from bs4 import BeautifulSoup
import requests

page = requests.get("https://books.toscrape.com/catalogue/page-1.html")
soup = BeautifulSoup(page.content, 'html.parser')

books_name = soup.find_all("a", "title")
print(books_name)

