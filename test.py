import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup

 
# read url from input
original_url = "https://www.xaa.edu.sg/admissions/book-school-tour/?utm_source=google&utm_medium=cpc&utm_term=&network=x&utm_campaign=&utm_content=&gad_source=1&gclid=Cj0KCQiA4Y-sBhC6ARIsAGXF1g4WP-JJ1NkyYP0a_5MY3rm3GyAGU-GwPFBM6ZuCdKQdl2bt3sB4mKYaAhXsEALw_wcB"

 
# to save urls to be scraped
unscraped = deque([original_url])
 
# to save scraped urls
scraped = set()
 
# to save fetched emails
emails = set()  
 
while len(unscraped):
    url = unscraped.popleft()  
    scraped.add(url)
 
    parts = urlsplit(url)
        
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if '/' in parts.path:
      path = url[:url.rfind('/')+1]
    else:
      path = url
 
    print("Crawling URL %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue
 
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+[a-z0-9\.\-+_]", response.text, re.I))
    emails.update(new_emails) 
 
    soup = BeautifulSoup(response.text, 'lxml')
 
    for anchor in soup.find_all("a"):
      if "href" in anchor.attrs:
        link = anchor.attrs["href"]
      else:
        link = ''
 
        if link.startswith('/'):
            link = base_url + link
        
        elif not link.startswith('http'):
            link = path + link

print(emails)