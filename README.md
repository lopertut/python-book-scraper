## Библеотеки:
* **BeautifulSoup** - для парсинга страниц
* **requests** - для получения доступа к странице
* **json** - для работы с json файлом
* **dicttoxml** - для работы с xml файлом

## Структура:
1. Импортируем все нужные библиотеки
2. Обьявляем переменные(json_books, xml_books, page_number и т.д.)
3. Заходим в цикл который проходит по заданому кол-во страниц
4. Заходим во вложенный цикл в котором извлекаем данный книг и записываем их в словари с небольшой сортировкой для каждого файла
5. После оканчание обоих циклов записаваем данные в books.json и books.xml

