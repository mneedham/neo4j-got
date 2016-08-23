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

def get_houses(character_id):
    print character_id
    file_name = character_id.split("/")[-1]
    wikia = BeautifulSoup(open("data/wikia/characters/{0}".format(file_name), "r"), "html.parser")
    allegiance_element = [tag for tag in select(wikia, 'h3') if tag.text == "Allegiance"]

    if len(allegiance_element) > 0:
        houses_elements = allegiance_element[0].next_sibling.next_sibling.contents
        return extract_houses(houses_elements)
    else:
        return []

def get_family(character_id):
    # print character_id
    file_name = character_id.split("/")[-1]
    wikia = BeautifulSoup(open("data/wikia/characters/{0}".format(file_name), "r"), "html.parser")
    family_element = [tag for tag in select(wikia, 'h3') if tag.text == "Family"]
    if len(family_element) > 0:
        family = family_element[0].next_sibling.next_sibling
        collapsed = select(family, "div.mw-collapsed")

        if len(collapsed) > 0:
            return extract_houses(select(family, "div.mw-collapsed")[0].contents)
        else:
            return extract_houses(family.contents)
    else:
        return []

def find_word(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search

# print get_houses("/wiki/Arya_Stark")
file_name = "Arya_Stark"
wikia = BeautifulSoup(open("data/wikia/characters/{0}".format(file_name), "r"), "html.parser")
allegiance_element = [tag for tag in wikia.find_all('h3') if tag.text == "Allegiance"]

print allegiance_element

next_element = allegiance_element[0].next_sibling
print next_element.name, type(next_element)

next_element = allegiance_element[0].next_sibling.next_sibling
print next_element.name, type(next_element)

# with open("data/characters_to_download.csv", "r") as characters_file, \
#      open("data/import/family_ties.csv", "w") as families_file:
#     reader = csv.reader(characters_file, delimiter = ",")
#     next(reader)
#
#     writer = csv.writer(families_file, delimiter = ",")
#     writer.writerow(["character1", "character2", "relationship", "type"])
#
#     for row in reader:
#         character = row[0]
#         for family in get_family(character):
#             family_member_id, family_member = family
#
#             if find_word("father")(family_member):
#                 type = "biological"
#                 if not any(x in family_member for x in ["father-in-law", "father-by-law", "father-by-marriage"]):
#                     if "legal father" in family_member:
#                         type = "legal"
#                     if "adoptive father" in family_member:
#                         type = "adoptive"
#
#                     writer.writerow([character, family_member_id, "father", type])
#
#             if find_word("mother")(family_member):
#                 if not any(x in family_member for x in ["mother-in-law", "step-mother", "cousin"]):
#                     writer.writerow([character, family_member_id, "mother", ""])
#
# with open("data/import/characters.csv", "r") as characters_file, \
#      open("data/import/allegiances.csv", "w") as allegiances_file:
#      reader = csv.reader(characters_file, delimiter = ",")
#      next(reader)
#
#      writer = csv.writer(allegiances_file, delimiter = ",")
#      writer.writerow(["character", "houseLink", "houseName"])
#      for row in reader:
#          character = row[0]
#          houses = get_houses(row[0])
#          for house in houses:
#              link = house[0].encode("utf-8") if house[0] else house[0]
#              name = house[1].encode("utf-8") if house[1] else house[1]
#              writer.writerow([character, link, name])
