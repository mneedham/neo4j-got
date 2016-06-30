from bs4 import BeautifulSoup, Tag

from bs4 import NavigableString
from soupselect import select
import bs4
import csv
import re
import sys

def extract_name(elements):
    value = ""
    for element in elements:
        if hasattr(element, "text"):
            value += element.text
        else:
            value += element
    return value

def extract_houses(elements):
    pre_parsed = []
    for element in elements:
        if element.name == "p":
            pre_parsed.append(Tag(name="br"))
            for item in list(element.children):
                pre_parsed.append(item)
        else:
            pre_parsed.append(element)

    items = []
    current = []
    for element in pre_parsed:
        # print element.name, element
        if element.name == "br":
            items.append(current)
            current = []
        else:
            current.append(element)

    items.append(current)

    houses = []
    for item in items:
        potential_link = [i for i in item if i.name == "a"]
        link = potential_link[0].get("href") if len(potential_link) > 0 else None
        name = extract_name(item)

        if link and name != "":
            houses.append((link, name))
    return houses

def process_character(character_id):
    print character_id
    file_name = character_id.split("/")[-1]
    wikia = BeautifulSoup(open("data/wikia/characters/{0}".format(file_name), "r"), "html.parser")
    allegiance_element = [tag for tag in select(wikia, 'h3') if tag.text == "Allegiance"]

    if len(allegiance_element) > 0:
        houses_elements = allegiance_element[0].next_sibling.next_sibling.contents
        return extract_houses(houses_elements)
    else:
        return []

with open("data/import/characters.csv", "r") as characters_file, \
     open("data/import/allegiances.csv", "w") as houses_file:
     reader = csv.reader(characters_file, delimiter = ",")
     next(reader)

     writer = csv.writer(houses_file, delimiter = ",")
     writer.writerow(["character", "houseLink", "houseName"])
     for row in reader:
         character = row[0]
         houses = process_character(row[0])
         for house in houses:
             link = house[0].encode("utf-8") if house[0] else house[0]
             name = house[1].encode("utf-8") if house[1] else house[1]
             writer.writerow([character, link, name])
