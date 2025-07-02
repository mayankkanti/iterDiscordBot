
from bs4 import BeautifulSoup as bs
import json, os, re, requests, urllib.parse
from typing import Tuple, List

def get_new_notices(file_path='./iter_bot/features/notice_board/data/seen_notices.json') -> Tuple[List[dict], List[dict]]:
    notice_board_url = 'https://www.soa.ac.in/iter-news-and-events'
    notices = []

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                seen_notices = json.load(f)
        except (json.JSONDecodeError, IOError):
            seen_notices = []
    else:
        seen_notices = []

    html = requests.get(notice_board_url)
    content = bs(html.content, 'html5lib')
    notice_block = content.find('div', attrs={'class': 'blog-basic-grid collection-content-wrapper'})

    for row in notice_block.find_all_next('h1', attrs={'class': 'blog-title'}):
        title = re.sub(r'\s+', ' ', row.a.text).strip()
        link = urllib.parse.urljoin(notice_board_url, row.a['href'])
        notices.append({'Title': title, 'Link': link})

    new_notices = [n for n in notices if n not in seen_notices]

    return new_notices, notices


def save_notices(notices: List[dict], file_path='./iter_bot/features/notice_board/data/seen_notices.json') -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(notices, f, indent=2)
