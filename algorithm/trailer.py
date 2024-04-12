import re

import urllib.request as url


def get_trailer_link(movie):
    str__movie = ""
    for i in movie:
        if i.isalpha():
            str__movie += i

    url_link = f"https://www.youtube.com/results?search_query={str__movie} trailer"
    url_link = url_link.replace(" ", "%20")

    print("URL:: ", url_link)

    html = url.urlopen(url_link)

    video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    print(video_id)

    return video_id[0]
