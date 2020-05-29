import requests
import urllib.request
import time
from bs4 import BeautifulSoup

talk_link = set()

next_page = "https://www.ted.com/talks"

while True:
    time.sleep(2)
    
    response = requests.get(next_page)
    
    next_page = None

    soup = BeautifulSoup(response.text, "html.parser")

    links_as = soup.findAll('a')
    
    for link_a in links_as:
        if 'a class=" ga-link" data-ga-context="talks"' in str(link_a):
            talk_link.add("https://www.ted.com"+link_a["href"]+"/transcript")
            print(talk_link)
        if 'rel="next"' in str(link_a):
            next_page = "https://www.ted.com"+link_a["href"]
    
    if next_page is None:
        break
        
print(len(talk_link))


