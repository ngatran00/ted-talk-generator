import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import string
from unidecode import unidecode

talk_links = set()

next_page = "https://www.ted.com/talks"

while True:
    time.sleep(2)
    
    response = requests.get(next_page)
    
    next_page = None

    soup = BeautifulSoup(response.text, "html.parser")

    links_as = soup.findAll('a')
    
    for link_a in links_as:
        if 'a class=" ga-link" data-ga-context="talks"' in str(link_a):
            talk_links.add("https://www.ted.com"+link_a["href"]+"/transcript?language=en")
        if 'rel="next"' in str(link_a):
            next_page = "https://www.ted.com"+link_a["href"]
    
    if next_page is None:
        break

data = []

i = 1

for talk_link in talk_links:
    print(i)
    time.sleep(2)

    response = requests.get(talk_link)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    author = None
    
    for meta in soup.findAll("meta"):
        if meta.get('name', '').lower() == "author":
            author = meta['content'].strip()
            author = author.translate(str.maketrans('', '', string.punctuation)) + " "
            author = unidecode(author)
            break
    
    if author is None:
        pass
        
    else:
                
        title = talk_link.split("/")[-2].replace("_", " ")
        
        title = title.replace(author.lower(), "", 1)
        
        link_ps = soup.findAll('p')

        script = ""

        for link_p in link_ps:
            if "TED.com translations are made possible by volunteer" in link_p.text:
                break
            script += (' '.join(str(link_p.text).split())) + "\n"
            
        data.append([title, script])
        
    i+=1

df = pd.DataFrame (data, columns = ["Title", "Script"])

df.to_csv('script.csv', encoding='utf-8', index=False)
