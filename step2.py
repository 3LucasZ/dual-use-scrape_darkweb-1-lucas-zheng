import requests
from urllib.parse import urljoin

TOR_SOCKS = "socks5h://127.0.0.1:9050"  # use 9150 if Tor Browser
proxies = {"http": TOR_SOCKS, "https": TOR_SOCKS}
headers = {"User-Agent": "Mozilla/5.0"}

ins = ["http://g7ejphhubv5idbbu3hb3wawrs5adw7tkx7yjabnf65xtzztgg4hcsqqd.onion",
       "http://archiveiya74codqgiixo33q62qlrqtkgmcitqx5u2oeqnmn5bpcbiyd.onion"]
outs = ["site1.html", "site2.html"]

for i in [0, 1]:
    url = ins[i]
    resp = requests.get(url, proxies=proxies, headers=headers, timeout=60)
    resp.raise_for_status()
    with open(outs[i], "w") as f:
        f.write(resp.text)
