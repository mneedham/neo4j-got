import bs4
import csv
import requests

import os

with open("data/characters_to_download.csv", "r") as episodes_file:
    reader = csv.reader(episodes_file, delimiter = ",")
    next(reader, None)

    for row in reader:
        name = row[0].split("/")[-1]
        download_location = "data/wikia/characters/{0}".format(name)

        if not os.path.isfile(download_location):
            print name, row[0]
            page = requests.get("http://gameofthrones.wikia.com{0}".format(row[0]))
            with open(download_location, 'wb') as test:
                test.write(page.content)
