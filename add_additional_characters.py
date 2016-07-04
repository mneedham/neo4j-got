# It only makes sense to call this script after the family ties have been calculated

from neo4j.v1 import GraphDatabase, basic_auth
import csv

# driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
# session = driver.session()
#
# rows = session.run("""load csv with headers from "file:///family_ties.csv" AS row
#                       OPTIONAL MATCH (character2:Character {id: row.character2})
#                       WITH row where character2 is  null
#                       return DISTINCT row.character2 AS missing""")

from sets import Set
chars = Set()
with open("data/characters_to_download.csv", "r") as characters_file:
    reader = csv.reader(characters_file, delimiter = ",")
    next(reader)

    for row in reader:
        link = row[0]
        chars.add(link)

new_chars = Set()

with open("data/import/family_ties.csv", "r") as families_file:
    reader = csv.reader(families_file, delimiter = ",")
    next(reader)

    for row in reader:
        character1 =  row[0]
        character2 =  row[1]
        if not character1 in chars:
            new_chars.add(character1)

        if not character2 in chars:
            new_chars.add(character2)

with open("data/characters_to_download.csv", "a") as characters_file:
    writer = csv.writer(characters_file, delimiter = ",")

    for char in new_chars:
        writer.writerow([char, ""])
