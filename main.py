import os
import requests
from bs4 import BeautifulSoup


def get_chapter_name(chapter_text):
    chapter_name_begin_idx = chapter_text.index('>') + 1
    chapter_name_end_idx = chapter_text.index('</h2>')
    return chapter_text[chapter_name_begin_idx:chapter_name_end_idx]


def cleanhtml(raw_html):
    cleantext = BeautifulSoup(raw_html, "lxml").text
    cleantext = cleantext.encode('ascii', 'ignore').decode()
    return cleantext


if __name__ == '__main__':
    base_url = 'https://www.core-econ.org/the-economy/book/text/'
    index_file = open("index.csv", "w", encoding='utf-8')
    index_file.write('filename,url\n')
    if not os.path.exists('pages'):
        os.mkdir("pages")
    for i in range(1, 23):
        if i < 10:
            content_url = base_url + '0' + str(i) + '.html'
        else:
            content_url = base_url + str(i) + '.html'
        print(content_url)
        response = requests.get(content_url)
        html_doc = response.text
        chapters = html_doc.split("<h2")
        file_name = str(i) + '_' + '1.html'
        chapter_file = open('pages/' + file_name, 'w', encoding='utf-8')
        chapter_file.write(cleanhtml(chapters[0]))
        chapter_file.close()
        index_file.write(file_name + ',' + content_url + '\n')
        for j in range(1, len(chapters)):
            chapters[j] = "<h2" + chapters[j]
            chapter_name = get_chapter_name(chapters[j])
            page_link = content_url + '#' + chapter_name.lower().replace(' ', '-').replace('.','')
            file_name = str(i) + '_' + str(j + 1) + '.html'
            chapter_file = open('pages/' + file_name, 'w', encoding='utf-8')
            chapter_file.write(cleanhtml(chapters[j]))
            chapter_file.close()
            index_file.write(file_name + ',' + page_link + '\n')
    index_file.close()

