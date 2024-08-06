import requests
import fake_headers
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = fake_headers.Headers(browser='chrome', os='win')
## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

main_html = requests.get('https://habr.com/ru/all/', 
                         headers=headers.generate()
                         ).text


main_soup = BeautifulSoup(main_html, features='lxml')

div_article_list = main_soup.find('div','tm-articles-list')

tags = div_article_list.find_all('article')

parsed_data = []

for article in tags:
    time_tag = article.find("time")
    pub_time = time_tag['datetime']

    h2_tag = article.find("h2")
    header = h2_tag.text.strip()

    a_tag = h2_tag.find("a")
    relative_link = a_tag['href']

    absolute_link = urljoin(f'https://habr.com/', relative_link)

    full_article_html = requests.get(
        absolute_link, 
        headers=headers.generate()
    ).text

    full_article_soup = BeautifulSoup(full_article_html, features='lxml')
    full_article_tag = full_article_soup.find('div', id='post-content-body')
    full_text = full_article_tag.text.strip()
    
    found_keywords = [keyword for keyword in KEYWORDS if keyword.lower() in header.lower() or keyword.lower() in full_text.lower()]
    
    if found_keywords:
        parsed_data.append({
            "pub_time": pub_time,
            'header': header,
            'link': absolute_link,
            'keywords': found_keywords,  # сохраняем найденные ключевые слова
            'text': full_text[:100]             
        })

print(parsed_data)


# div_class="tm-articles-list"
# h2 class="tm-title tm-title_h2"
# a href="/ru/articles/834016/"
# time datetime="2024-08-05T20:47:10.000Z"