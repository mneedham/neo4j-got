from bs4 import BeautifulSoup
from soupselect import select
import bs4
import csv

wikipedia = BeautifulSoup(open("data/wikipedia/No_One_(Game_of_Thrones)", "r"), "html.parser")
wikia = BeautifulSoup(open("data/wikia/No_One", "r"), "html.parser")

rows = select(wikipedia, "table.infobox tr")

for row in rows:
    heading = select(row, "th")
    if len(heading) > 0:
        raw_title = select(heading[0], "b")
        if len(raw_title) > 0:
            title = raw_title[0].text
        if heading[0].text.strip() == "Episode no.":
            season, episode = select(row, "td")[0].text.strip().split("\n")

season =  season.replace("Season", "").strip()
episode = episode.replace("Episode ", "").strip()

characters = select(wikia, "table li")

with open("data/import/overview.csv", "w") as overview_file:
    writer = csv.writer(overview_file, delimiter = ",")
    writer.writerow(["season", "episode", "title"])
    writer.writerow([season, episode, title])

with open("data/import/characters.csv", "w") as characters_file:
    writer = csv.writer(characters_file, delimiter = ",")
    writer.writerow(["actor", "character", "season", "episode"])

    for raw_character in characters:
        actor, character = [item.strip().replace("\n", "") for item in raw_character.text.replace(u'\xa0', u' ').split(" as ")]
        writer.writerow([actor.encode("utf-8"), character, season, episode])
