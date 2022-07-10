"""
Возможно небольшое ожидание из-за скорости интернета
"""

import requests
from bs4 import BeautifulSoup

url = 'https://inlnk.ru/jElywR'


## переход на следующую страницу
def go_next_page(sub):
    next_page = sub.find_all("a", string="Следующая страница")
    r = requests.get('https://ru.wikipedia.org' + next_page[0]["href"])
    return BeautifulSoup(r.content, features="html.parser")


## подсчет количества назвваний для каждой буквы на всех страницах
def get_count_wiki(url, stop_letter):
    letters = {}
    letter = ""

    r = requests.get(url)
    page = BeautifulSoup(r.content, features="html.parser")

    while letter != stop_letter:
        res = page.find(id="mw-pages")
        
        # ищем все заголовки букв на странице
        headers_leter = res.find_all(class_="mw-category-group") 

        for header in headers_leter:
            # для каждой буквы сичтаем количество названий в списке
            count = len(header.find_all("li")) 

            letter = header.find("h3").text
            if letter in letters:
                letters[letter] += count
            else:
                letters[letter] = count

        page = go_next_page(res)
    
    return letters


##вывод результата
def print_res(d):
    for key, value in d.items():
        print("{0}: {1}".format(key,value))


if __name__ == "__main__":
    print_res(get_count_wiki(url, "Я"))