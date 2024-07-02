import datetime
import os

from bloombergapa import get_file_data, get_file_list

BASE_FOLDER = "./data/bloomberg"


now = datetime.datetime.now()
time_identifier = now.strftime("%Y-%m-%d:%H.%M.%S")
destination_folder = BASE_FOLDER + "/" + str(time_identifier)

os.makedirs(destination_folder, exist_ok=True)

for filename, download_link in get_file_list():
    data = get_file_data(download_link)
    with open(f"{destination_folder}/{filename}", "wt") as f:
        f.write(data)
