'''
brew install tor
brew services start tor
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/
You should see: "Congratulations. This browser is configured to use Tor."
pip install "requests[socks]"  
'''
