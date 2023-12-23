import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from urllib.parse import urljoin
from googlesearch import search
from email_validator import validate_email, EmailNotValidError
from pathlib import Path 
from pyisemail import is_email
import stopit

NAMES = r'C:\Users\david\Documents\schoolsemails\cleanednames.txt'
EMAILS = r'C:\Users\david\Documents\schoolsemails\emails.txt'

def perform_search(query)-> []:
    return list(search(query, num=1, stop=1, pause=.5))[0]

def save_to_file(string: str, file: Path)-> None:
    open_file = file.open('a')
    open_file.write(string+ '\n')
    open_file.close() 

def get_response(url: str) ->requests.get: 
    try:
        return requests.get(url)
    except:
        pass 

def find_emails(response: requests.get) -> set(): 
    return set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+[a-z0-9\.\-+_]", response.text, re.I))

def names_list()-> []:
    names = Path(NAMES)
    names = names.open('r')
    names_list = names.readlines()
    names.close()
    return names_list

def save_emails(file: Path, emails: set()) -> None: 
    for email in emails: 
        save_to_file(email, file)

def get_connecting(url: str) -> []:
    return_list = set()
    return_list.add(url) 
    response = requests.get(url)
    url_parts = urlsplit(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and href.startswith('http'):
            return_list.add(href)
        else:
            complete_link = urljoin(url_parts.netloc, href)
            return_list.add(complete_link)
    return list(return_list)

def get_all_connecting(url_list: []) ->[]:
        'not yet implemented'
        pass
        
def validate_emails(emails:[])-> []:
    valid_emails = []
    for email in emails:
        if is_email(email, check_dns=True):
            try:
                emailinfo = validate_email(email, check_deliverability=True)
                valid_emails.append(email)
            except:
                pass
    return valid_emails 


def inner_for(url:str, emails: Path)-> None:
    print(url)
    response = get_response(url)
    save_emails(emails, validate_emails(find_emails(response)))

def main() -> None:
    emails = Path(EMAILS)
    number = 1 
    for name in names_list():
        print(number)
        number += 1
        with stopit.ThreadingTimeout(60):
            try:
                print(name)
                name = name.strip()
                starting_url = perform_search(name)
                print('search completed')
                for url in list(get_connecting(starting_url)):
                    with stopit.ThreadingTimeout(10):
                        try:
                            inner_for(url,emails)
                            print('parse completed')
                        except stopit.TimeoutException:
                            print('Timeout occurred for: ' + url)
                        except:
                            print('error with: ' + url)
            except: 
                print("error with: " + name)

def top_level_main() -> None:
    emails = Path(EMAILS)
    number = 1 
    for name in names_list():
        print(number)
        number += 1
        try:
            print(name)
            name = name.strip()
            starting_url = perform_search(name)
            print('search completed')
            try:
                 with stopit.ThreadingTimeout(10):
                    inner_for(starting_url,emails)
                    print('parse completed')
            except:
                print('error with: ' + starting_url)
        except: 
            pass

def davids_tests()-> None:
    emails = Path(r'C:\Users\david\Documents\schoolsemails\davidsemails')
    davids_urls = Path(r'C:\Users\david\Documents\schoolsemails\davids').open('r')
    line_number = 1
    for line in davids_urls.readlines():
        print(str(line_number) + '     ')
        line_number += 1
        try:
            starting_url = line.strip()
            for url in list(get_connecting(starting_url)):
                print(url) 
                response = get_response(url)
                save_emails(emails, validate_emails(find_emails(response)))
        except: 
            pass
            

main()


