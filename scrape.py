from bs4 import BeautifulSoup
from bs4 import NavigableString
from soupselect import select
import bs4
import csv

wikipedia = BeautifulSoup(open("data/wikipedia/55", "r"), "html.parser")
wikia = BeautifulSoup(open("data/wikia/55", "r"), "html.parser")

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

for section in [section for section in  select(wikipedia, "h3 span.mw-headline") if not section.text in ["Writing", "Casting", "Filming", "Ratings", "Critical reception"] ]:

    print section.get("id"), section.text
    content = []
    next_bit = section.parent.next_sibling
    while True:
        if next_bit is None:
            next_bit = next_bit.next_sibling
            continue
        if next_bit.name in ["h2", "h3"]:
            break
        else:
            content.append(next_bit)
            next_bit = next_bit.next_sibling

    for item in content:
        print item
        if item is not NavigableString:
            print select(item, "a")


import sys
sys.exit(1)

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
