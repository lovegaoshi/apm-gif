import requests
from urllib.parse import urlparse
import time
import logging
import os
import json
from pathlib import Path
from bs4 import BeautifulSoup

def download_walfie(result_dict, folder):
    for url in result_dict.keys():
        logging.info(f'downloading {result_dict[url]} of {folder}')
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join('gifs', folder, f'{result_dict[url]}{os.path.splitext(url)[1]}'), 'wb') as f:
                f.write(response.content)
        time.sleep(5)
        

def scrape_walfie(url, result_string = None, result_dict = None, dedup = True):
    logging.info(f'scraping {url}')
    def strip_URL_search_params(img_url):
        parsed_url = urlparse(img_url)
        return f'https://{parsed_url.netloc}{parsed_url.path}'

    if result_string == None:
        result_string = []
    if result_dict == None:
        result_dict = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    duplicate = False
    parsed_walfie_gifs = [[strip_URL_search_params(x['src']), x['title']] for x in soup.find_all(class_='attachment-rebalance-archive wp-post-image')]
    time.sleep(3)
    for i in parsed_walfie_gifs:
        if i[0] in result_string:
            duplicate = True
        else: 
            result_string.append(i[0])
            result_dict[i[0]] = i[1]
    if duplicate and dedup:
        logging.info(f'finished scraping {url} due to duplication')
        return result_string, result_dict
    next_page = soup.find(class_='nav-previous')
    if next_page == None:
        logging.info(f'finished scraping {url}; end of pages')
        return result_string, result_dict
    logging.info(f'continue scraping {url}')
    return scrape_walfie(next_page.a['href'], result_string, result_dict, dedup)

def save_walfie(tag):
    Path(os.path.join('gifs', tag)).mkdir(parents=True, exist_ok=True)
    try:
        with open(os.path.join('gifs', tag, 'data.json')) as f:
            result_string, result_dict = json.load(f)
    except:
        result_string =  None
        result_dict = {}
    result_string, result_dict2 = scrape_walfie(f'https://walfiegif.wordpress.com/tag/{tag}', result_string=result_string, dedup=True)
    download_walfie(result_dict2, tag)
    result_dict.update(result_dict2)
    with open(os.path.join('gifs', tag, 'data.json'), 'w') as f:
        json.dump([result_string, result_dict], f, indent=4)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    save_walfie('amelia-watson')
    save_walfie('gawr-gura')
    save_walfie('ninomae-inanis')