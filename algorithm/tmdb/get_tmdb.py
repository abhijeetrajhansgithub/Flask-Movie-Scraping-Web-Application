import requests
from bs4 import BeautifulSoup
import time


def get_actual_link(movie_prompt):
    print("inside get_actual_link")
    url = "https://www.themoviedb.org/search?query="
    movie = movie_prompt.replace(" ", "+")

    url = url + movie

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    with requests.Session() as session:
        session.headers.update(headers)

        # make a request
        response = session.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            result_div = soup.find('a', class_='result')
            if result_div:
                href = result_div['href']
                return href

        else:
            print("Failed to retrieve data from the server")
            return []


# Example usage:
# movie_prompt = input("Enter the movie name: ")
# movie_link = get_actual_link(movie_prompt)
# print("Movie links:", "https://www.themoviedb.org/" + movie_link)
