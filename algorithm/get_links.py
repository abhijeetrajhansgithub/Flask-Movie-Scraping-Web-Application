def get_links(anchors):
    page = "https://en.wikipedia.org"
    links = []
    for i in anchors:
        try:
            if i[1].startswith("/wiki/"):
                links.append([i[0], page + i[1]])
        except IndexError:
            pass
        except TypeError:
            pass
        except AttributeError:
            pass
        except ValueError:
            pass

    return links
