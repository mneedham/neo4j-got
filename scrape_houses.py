from bs4 import BeautifulSoup, Tag

from bs4 import NavigableString
from soupselect import select
import bs4
import csv
import re
import sys

wikia = BeautifulSoup(open("data/Great_Houses", "r"), "html.parser")

with open("data/import/houses.csv", "w") as houses_file:
     writer = csv.writer(houses_file, delimiter = ",")
     writer.writerow(["link", "name"])

     for house in select(wikia, "li b a"):
         writer.writerow([house.get("href"), house.text])
