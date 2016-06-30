import bs4
import csv
import requests

with open("data/import/characters.csv", "r") as episodes_file:
    reader = csv.reader(episodes_file, delimiter = ",")
    next(reader, None)

    for row in reader:
        name = row[0].split("/")[-1]
        print name, row[0]

        page = requests.get("http://gameofthrones.wikia.com{0}".format(row[0]))
        with open("data/wikia/characters/{0}".format(name), 'wb') as test:
            test.write(page.content)
