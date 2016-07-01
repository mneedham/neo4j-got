import bs4
import csv
import requests

with open("data/import/houses.csv", "r") as houses_file:
    reader = csv.reader(houses_file, delimiter = ",")
    next(reader, None)

    for row in reader:
        print row

        page = requests.get("http://gameofthrones.wikia.com{0}".format(row[0]))
        with open("data/wikia/houses/{0}".format(row[1]), 'wb') as test:
            test.write(page.content)
