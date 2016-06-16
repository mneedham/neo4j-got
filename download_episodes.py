import bs4
import csv
import requests

with open("data/wikiaEpisodes.csv", "r") as episodes_file:
    reader = csv.reader(episodes_file, delimiter = ",")
    next(reader, None)

    for row in reader:
        print row

        page = requests.get(row[1])
        with open("data/wikia/{0}".format(row[0]), 'wb') as test:
            test.write(page.content)

with open("data/wikipediaEpisodes.csv", "r") as episodes_file:
    reader = csv.reader(episodes_file, delimiter = ",")
    next(reader, None)

    for row in reader:
        print row

        page = requests.get(row[1])
        with open("data/wikipedia/{0}".format(row[0]), 'wb') as test:
            test.write(page.content)
