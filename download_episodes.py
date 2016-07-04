import bs4
import csv
import requests
import os

with open("data/wikiaEpisodes.csv", "r") as episodes_file:
    reader = csv.reader(episodes_file, delimiter = ",")
    next(reader, None)

    for row in reader:
        print row
        file_name = "data/wikia/{0}".format(row[0])
        if not os.path.isfile(file_name):
            print "downloading..."
            page = requests.get(row[1])
            with open(file_name, 'wb') as test:
                test.write(page.content)

with open("data/wikipediaEpisodes.csv", "r") as episodes_file:
    reader = csv.reader(episodes_file, delimiter = ",")
    next(reader, None)

    for row in reader:
        print row
        file_name = "data/wikipedia/{0}".format(row[0])
        if not os.path.isfile(file_name):
            print "downloading..."
            page = requests.get(row[1])
            with open(file_name, 'wb') as test:
                test.write(page.content)
