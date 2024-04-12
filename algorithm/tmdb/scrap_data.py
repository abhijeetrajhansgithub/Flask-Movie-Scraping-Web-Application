import requests
from bs4 import BeautifulSoup


def scrap_data(movie):
    from algorithm.tmdb.get_tmdb import get_actual_link

    link = get_actual_link(movie)

    link = "https://www.themoviedb.org/" + link
    print(link)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    with requests.Session() as session:
        session.headers.update(headers)

        # make a request
        response = session.get(link)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.find('h2').text

            image = soup.find('img', class_='poster w-[100%]').get('src')

            certification = soup.find('span', class_='certification').text

            description = soup.find('div', class_='overview').text

            genre = soup.find('span', class_='genres').text

            profile = soup.find('li', class_='profile').text

            profile_images = soup.find_all('img', class_='profile w-[100%]')

            rating = soup.find('div', class_='user_score_chart')
            rating = str(rating.get('data-percent'))

            ul_element = soup.find('ul', class_='consensus_reaction_items ml-4')

            # Find all img tags within the ul element
            if ul_element:
                img_tags = ul_element.find_all('img')
                # Extract src attributes from img tags
                srcs = [img['src'] for img in img_tags]
                print("Image sources:", srcs)

            cast = []
            alt = []

            for img in profile_images:
                src = img['src']
                alt_ = img['alt']

                cast.append(src)
                alt.append(alt_)

            print(image, certification, description, genre, profile)

            print(cast)
            print(alt)

            dict_ = {
                'title': title,
                'image': image,
                'certification': certification,
                'description': description,
                'genre': genre,
                'profile': profile,
                'cast': cast,
                'alt': alt,
                'rating': rating
            }

            return dict_
        else:
            print("Failed to retrieve data from the server")
            return []


def extract_images_and_data():
    url = "https://www.themoviedb.org/movie?page="
    images_mapping = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    with requests.Session() as session:
        session.headers.update(headers)

        for page_num in range(1, 100):  # Iterate through pages from 1 to 50
            page_url = f"{url}{page_num}"  # Construct the URL for each page
            response = session.get(page_url)

            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find the class="media_items results"
                media_items = soup.find('div', class_='media_items results')

                if media_items:
                    # Find all div elements with class="card style_1"
                    cards = media_items.find_all('div', class_='card style_1')

                    # find anchor tags with class='image' and get the href and title as well
                    for card in cards:
                        # find anchor tags with class='image' and get the href and title as well
                        tag = card.find('a', class_='image')
                        href = tag['href']
                        title = tag['title']

                        img = tag.find('img')
                        src = img['src']

                        images_mapping.append({'title': title, 'href': href, 'src': src})

    return images_mapping

