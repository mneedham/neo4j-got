import csv

from bs4 import BeautifulSoup, Tag
from soupselect import select

with open("data/characters_to_download.csv", "r") as characters_download_file, \
     open("data/import/characters.csv", "w") as characters_file:

     reader = csv.reader(characters_download_file, delimiter = ",")
     next(reader)

     writer = csv.writer(characters_file, delimiter = ",")
     writer.writerow(["link", "character"])

     for row in reader:
         file_name = row[0].split("/")[-1]
         wikia = BeautifulSoup(open("data/wikia/characters/{0}".format(file_name), "r"), "html.parser")

         name_element = select(wikia, "h1")
         writer.writerow([row[0], name_element[0].text.strip()])
