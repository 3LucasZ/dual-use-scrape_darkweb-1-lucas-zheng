import json
import re
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import PhoneNumberMatcher, PhoneNumberFormat
import idna

### EMAIL ###


def extract_emails(text: str, soup):
    results = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    return results


# USERNAMES
# From links
SOCIAL_PATTERNS = [
    ('twitter/x',
     re.compile(r'https?://(?:www\.)?(?:twitter\.com|x\.com)/([A-Za-z0-9_]{1,15})(?:[/?#]|$)')),
    ('instagram', re.compile(
        r'https?://(?:www\.)?instagram\.com/([A-Za-z0-9._]{1,30})(?:[/?#]|$)')),
    ('github', re.compile(
        r'github\.com/([A-Za-z0-9-]{1,39})(?:[/?#]|$)')),
    ('reddit', re.compile(
        r'https?://(?:www\.)?reddit\.com/user/([A-Za-z0-9_-]{3,20})(?:[/?#]|$)')),
    ('telegram', re.compile(
        r'https?://(?:t\.me|telegram\.me)/([A-Za-z0-9_]{5,32})(?:[/?#]|$)')),
    ('mastodon', re.compile(
        r'https?://[^/\s]+/@([A-Za-z0-9_\.]{1,30})(?:[/?#]|$)')),
]

# @handles in text
HANDLE_REGEX = re.compile(r'(?<!\w)@([A-Za-z0-9_\.]{2,30})(?!\w)')


def extract_usernames(text: str, soup: BeautifulSoup):
    results = set()
    # From social links
    for a in soup.find_all('a', href=True):
        href = a['href']
        for _, rx in SOCIAL_PATTERNS:
            m = rx.search(href)
            if m:
                results.add(m.group(1))
    # From @handles in text
    for m in HANDLE_REGEX.finditer(text):
        handle = m.group(1)
        results.add(handle)
    return results

# PHONE NUMBERS


def extract_phone_numbers(text: str, soup: BeautifulSoup, default_region: str = 'US'):
    results = set()
    # tel: links
    if soup:
        for a in soup.select('a[href^="tel:"]'):
            raw = a.get('href', '')[4:]
            try:
                num = phonenumbers.parse(raw, default_region)
                if phonenumbers.is_possible_number(num) and phonenumbers.is_valid_number(num):
                    results.add(phonenumbers.format_number(
                        num, PhoneNumberFormat.E164))
            except Exception:
                pass
    # text
    for match in PhoneNumberMatcher(text, default_region or None):
        num = match.number
        if phonenumbers.is_possible_number(num) and phonenumbers.is_valid_number(num):
            results.add(phonenumbers.format_number(
                num, PhoneNumberFormat.E164))
    return results


def text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    for t in soup(['script', 'style', 'noscript']):
        t.extract()
    return soup.get_text(' ', strip=True), soup


def filter_list(l):
    new_l = []
    for el in l:
        if "702" in el or "jeff" in el:
            new_l.append(el)
    return new_l


def extract_all(html: str) -> dict:
    text, soup = text_from_html(html)
    emails = extract_emails(text, soup)
    usernames = extract_usernames(text, soup)
    phones = extract_phone_numbers(text, soup)
    return {
        'emails': filter_list(sorted(emails)),
        'usernames': filter_list(sorted(usernames)),
        'phone_numbers': filter_list(sorted(phones)),
    }


def extract_paths(paths):
    htmls = []
    for path in paths:
        with open(path, 'r') as file:
            html = file.read()
            htmls.append(html)
    ret = {}
    for html in htmls:
        ret = {**ret, **extract_all(html)}
    return ret


if __name__ == "__main__":
    paths = ["site1.html", "site2.html", "custom.html"]
    ret = extract_paths(paths)

    with open('result.json', 'w') as fp:
        json.dump(ret, fp, indent=True)
    print(ret)
