from bs4 import BeautifulSoup, Tag
from soupselect import select
import bs4
import csv
import re

wikia = BeautifulSoup(open("data/Great_Houses", "r"), "html.parser")

houses = {}
for house in select(wikia, "li b a"):
    houses[house.get("href")] =  house.text

with open("data/import/allegiances.csv", "r") as allegiances_file:
    reader = csv.reader(allegiances_file, delimiter = ",")
    next(reader)

    for row in reader:
        if row[2].startswith("House"):
            if not houses.get(row[1]):
                text = re.match("([^\(\-]*)", row[2]).groups()[0]
                houses[row[1]] = text

with open("data/import/houses.csv", "w") as houses_file:
     writer = csv.writer(houses_file, delimiter = ",")
     writer.writerow(["link", "name"])

     for house in houses:
         writer.writerow([house, houses[house]])
