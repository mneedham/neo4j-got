from bs4 import BeautifulSoup
from bs4 import NavigableString
from soupselect import select
import bs4
import csv

wikia = BeautifulSoup(open("data/Category:Episodes", "r"), "html.parser")
wikipedia = BeautifulSoup(open("data/List_of_Game_of_Thrones_episodes", "r"), "html.parser")

rows = select(wikia, "div#mw-content-text ul li")

with open("data/wikiaEpisodes.csv", "w") as episodes_file:
    writer = csv.writer(episodes_file, delimiter = ",")
    writer.writerow(["episodeNumber", "link"])

    episode_number = 1
    for row in rows:
        if row.text.startswith("Ep"):
            maybe_link = select(row, "a")
            if len(maybe_link) > 0:
                writer.writerow([episode_number, "http://gameofthrones.wikia.com{0}".format(maybe_link[0].get("href"))])
                episode_number += 1

    writer.writerow([56, "http://gameofthrones.wikia.com/wiki/Blood_of_My_Blood"])
    writer.writerow([57, "http://gameofthrones.wikia.com/wiki/The_Broken_Man"])
    writer.writerow([58, "http://gameofthrones.wikia.com/wiki/No_One"])

rows = select(wikipedia, "table tr.vevent")

with open("data/wikipediaEpisodes.csv", "w") as episodes_file:
    writer = csv.writer(episodes_file, delimiter = ",")
    writer.writerow(["episodeNumber", "link"])

    for row in rows:
        title_cell = select(row, "td.summary a")[0]
        episode_number = select(row, "th")[0].text
        writer.writerow([episode_number, "https://en.wikipedia.org{0}".format(title_cell.get("href"))])
