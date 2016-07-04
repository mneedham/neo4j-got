# It only makes sense to call this script after the family ties have been calculated

from neo4j.v1 import GraphDatabase, basic_auth
import csv

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""load csv with headers from "file:///family_ties.csv" AS row
                      OPTIONAL MATCH (character2:Character {id: row.character2})
                      WITH row where character2 is  null
                      return DISTINCT row.character2 AS missing""")

with open("data/import/characters.csv", "a") as characters_file:
    writer = csv.writer(characters_houses_file, delimiter = ",")

    for row in rows:
        row = row["row"]
        for row in rows:
            writer.writerow([row["missing"], ""])
