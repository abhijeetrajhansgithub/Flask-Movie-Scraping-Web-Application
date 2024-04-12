from typing import Any
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from algorithm.nltk.filter_text import clean_text_list
from algorithm.get_links import get_links


def get_wiki_details(movie_name, method=1) -> tuple[list[list[str]], list[list[str | Any]]]:
    movie_name = [word for word in movie_name.split()]
    name = [movie_name[0].capitalize()]

    for token in movie_name[1:]:
        if token not in ("in", "the", "a", "an", "and", "or", "to", "of", "for"):
            name.append(token.capitalize())
        else:
            name.append(token)

    movie_name = ' '.join(name)

    wiki_url = None

    if method == 1:
        wiki_url = f"https://en.wikipedia.org/wiki/{quote(movie_name.replace(' ', '_'))}_%28film%29"
    else:
        wiki_url = f"https://en.wikipedia.org/wiki/{movie_name.replace(' ', '_')}"

    response = requests.get(wiki_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        main_list = []
        h2_tags = soup.find_all('h2')

        n_p_tags_to_extract = 10

        for h2_tag in h2_tags:
            sub_list = [h2_tag.text]

            try:
                next_p_tags = h2_tag.find_next_siblings('p', limit=n_p_tags_to_extract)
            except AttributeError:
                continue

            # Print the text content of each <p> tag
            for p_tag in next_p_tags:
                sub_list.append(p_tag.text)

            main_list.append(sub_list)

        anchor_tags_main_list = []
        # Find all anchor tags
        anchor_tags = soup.find_all('a')

        # Print the text and href attributes of each anchor tag
        for anchor_tag in anchor_tags:
            text_content = anchor_tag.text
            href_content = anchor_tag.get('href')
            anchor_tags_main_list.append([text_content, href_content])

        return main_list, anchor_tags_main_list

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def get_wiki_summary(movie_name, method=1) -> list[str]:
    movie_name = [word for word in movie_name.split()]
    name = [movie_name[0].capitalize()]

    for token in movie_name[1:]:
        if token not in ("in", "the", "a", "an", "and", "or", "to", "of", "for"):
            name.append(token.capitalize())
        else:
            name.append(token)

    movie_name = ' '.join(name)

    wiki_url = None
    if method == 1:
        print("Inside method 1")
        wiki_url = f"https://en.wikipedia.org/wiki/{quote(movie_name.replace(' ', '_'))}_%28film%29"
    else:
        wiki_url = f"https://en.wikipedia.org/wiki/{movie_name.replace(' ', '_')}"

    print(wiki_url)

    response = requests.get(wiki_url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('table', {'class': 'infobox vevent'})
        if content:
            # Extract text from all the table row tags
            rows = content.find_all('tr')
            for row in rows:
                row_text = row.get_text(strip=True)
                print("Row text: ", row_text)
                data.append(row_text)
        else:
            print("Table with class 'infobox vevent' not found.")

        print("Inside data: ", data)

        return data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def run_basic_text_extraction(movie_name__) -> list[list[str]]:

    try:
        paragraphs, anchors = get_wiki_details(movie_name__)
        links = get_links(anchors)
        cleaned_paragraphs = []

        for paragraph in paragraphs:
            cleaned_paragraphs.append(clean_text_list(paragraph))

        return [cleaned_paragraphs, links]
    except TypeError:
        try:
            paragraphs, anchors = get_wiki_details(movie_name__, 2)
            links = get_links(anchors)
            cleaned_paragraphs = []

            for paragraph in paragraphs:
                cleaned_paragraphs.append(clean_text_list(paragraph))

            return [cleaned_paragraphs, links]
        except TypeError:
            return []


def run_precise_text_extraction(movie_name__) -> list[str]:
    print("Here :: 2", get_wiki_summary(movie_name__))
    return get_wiki_summary(movie_name__)

