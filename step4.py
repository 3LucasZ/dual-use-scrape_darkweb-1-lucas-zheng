import re
import unicodedata
import requests
from bs4 import BeautifulSoup
import re


def filter_paths(paths):
    htmls = []
    for path in paths:
        with open(path, 'r') as file:
            html = file.read()
            htmls.append(html)
    return filter_text(htmls)


def filter_text(htmls):
    ret = []
    for html in htmls:
        soup = BeautifulSoup(html)
        body_text = soup.get_text(" ", strip=True)
        # print(body_text)
        x = re.findall("\S*DEF CON\S*", body_text)
        y = re.findall("\S*onion\S*", body_text)
        ret.extend(x)
        ret.extend(y)
    return ret


if __name__ == "__main__":
    paths = ["site1.html", "site2.html"]
    ret = filter_paths(paths)
    print(ret)
