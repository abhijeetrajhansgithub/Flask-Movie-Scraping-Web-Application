import wikipedia


def get_movie_details(movie_title):
    try:
        # Search for the Wikipedia page of the movie
        page = wikipedia.page(movie_title)

        # Extract summary and URL
        summary = page.summary
        url = page.url

        # You can extract more details as needed
        # For example, page.content will give you the full content of the page

        return {
            'title': page.title,
            'summary': summary,
            'url': url
        }
    except wikipedia.exceptions.PageError:
        return None


# Example usage
movie_title = "Inception movie"
movie_details = get_movie_details(movie_title)
if movie_details:
    print("Title:", movie_details['title'])
    print("Summary:", movie_details['summary'])
    print("URL:", movie_details['url'])
else:
    print("Movie not found on Wikipedia.")
