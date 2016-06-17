from bs4 import BeautifulSoup
from bs4 import NavigableString
from soupselect import select
import bs4
import csv

def process_episode(episode_id):
    wikipedia = BeautifulSoup(open("data/wikipedia/{0}".format(episode_id), "r"), "html.parser")
    wikia = BeautifulSoup(open("data/wikia/{0}".format(episode_id), "r"), "html.parser")

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

    actors_locations = []
    for section in [section for section in  select(wikipedia, "h3 span.mw-headline") if not section.text in ["Writing", "Casting", "Filming", "Ratings", "Critical reception"] ]:
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

        actors = []
        for item in content:
            if item is not NavigableString:
                try:
                    for actor in select(item, "a"):
                        actors.append(actor.text)
                except AttributeError:
                    pass

        for actor in actors:
            actors_locations.append([episode_id, section.get("id").encode("utf-8"), section.text.encode("utf-8"), actor.encode("utf-8")])

    return {
        'season': season,
        'episode': episode,
        'characters': characters,
        'actors_locations': actors_locations,
        'title': title
        }

episodes = {}

for episode_id in range(1, 10):
    episodes[episode_id] = process_episode(episode_id)

with open("data/import/overview.csv", "w") as overview_file:
    writer = csv.writer(overview_file, delimiter = ",")
    writer.writerow(["episodeId", "season", "episode", "title"])

    for episode_id in episodes:
        season = episodes[episode_id]['season']
        episode = episodes[episode_id]['episode']
        title = episodes[episode_id]['title']
        writer.writerow([episode_id, season, episode, title])

with open("data/import/characters.csv", "w") as characters_file:
    writer = csv.writer(characters_file, delimiter = ",")
    writer.writerow(["actor", "character", "episodeId"])

    for episode_id in episodes:
        characters = episodes[episode_id]['characters']
        for raw_character in characters:
            actor, character = [item.strip().replace("\n", "") for item in raw_character.text.replace(u'\xa0', u' ').split(" as ")]
            writer.writerow([actor.encode("utf-8"), character, episode_id])

with open("data/import/locations.csv", "w") as locations_file:
    writer = csv.writer(locations_file, delimiter = ",")
    writer.writerow(["episodeId", "locationId", "locationName", "actor"])

    for episode_id in episodes:
        actors_locations = episodes[episode_id]['actors_locations']
        for actor_location in actors_locations:
            writer.writerow(actor_location)
