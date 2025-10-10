from bs4 import BeautifulSoup


def scrape(path):
    with open(path, 'r') as file:
        content = file.read()
    soup = BeautifulSoup(content)
    title = soup.title.string.strip() if soup.title else ""
    main_text = soup.get_text(" ", strip=True)
    print("Title:", title)
    print("Sample:", main_text[:300])


if __name__ == "__main__":
    scrape("site1.html")
