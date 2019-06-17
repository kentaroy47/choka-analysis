"""
from https://github.com/ohbarye/choka-scraper
@ohbarye
"""


import textwrap
import requests
from bs4 import BeautifulSoup


def fetch_choka_list(url, facility_id, max_page=None, choka_list=[], page_number=1):
    print(f"Fetching page {page_number}...")

    session = requests.session()

    post_data = {
        "s": facility_id,
        "pageID": page_number,
    }

    res = session.post(url, data=post_data)
    soup = BeautifulSoup(res.text, "html.parser")
    
    return soup
    


def format_choka_box(choka_box):
    return {
            "date":    choka_box.find(class_="chokaBox-headerList").get_text().strip(),
            "summary": choka_box.find(class_='speech-bubble').get_text().strip(),
            }

def print_choka(choka_list):
    for choka in choka_list:
        print(textwrap.dedent(f'''
        ## {choka["date"]}
        {choka["summary"]}

        ''').strip())

if __name__ == "__main__":
    url = "https://www.fishing-v.jp/choka/choka_detail.php"
    facility_id = "11284"
    max_page = 3

    choka_list = fetch_choka_list(url, facility_id, max_page=max_page)

    print_choka(choka_list)
