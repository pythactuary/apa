"""Downloads all the text files from the Bloomberg APA website"""

import datetime
import os

import requests
import bs4

BASE_URL = "https://www.bloombergapa.com"
BASE_FOLDER = "apa/bloomberg"


def get_file_list() -> list[tuple[str, str]]:
    """Gets a list of the file names and links to the files

    Returns:
    list of tuples of (file_name, download_link)
    """
    history_files_page = requests.get(f"{BASE_URL}/historyfiles")
    soup = bs4.BeautifulSoup(history_files_page.content, "html.parser")
    link_list: list[bs4.PageElement] = soup.find(class_="col-12 file-list").find_all(
        "a"
    )
    return [(link.text, link["href"]) for link in link_list]


def get_file_data(download_link) -> str:
    """Get the data from the link"""
    response = requests.get(BASE_URL + download_link)
    # split out the header
    HEADER_SEPARATOR = "\n\n\n\n\n\n\n\n"
    data = response.content.decode().split(HEADER_SEPARATOR)[1]
    return data


now = datetime.datetime.now()
time_identifier = now.strftime("%Y-%m-%d:%H.%M.%S")
destination_folder = BASE_FOLDER + "/" + str(time_identifier)

os.makedirs(destination_folder, exist_ok=True)

for filename, download_link in get_file_list():
    data = get_file_data(download_link)
    with open(f"{destination_folder}/{filename}", "wt") as f:
        f.write(data)
