# It only makes sense to call this script after the family ties have been calculated

from neo4j.v1 import GraphDatabase, basic_auth
import csv

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""load csv with headers from "file:///family_ties.csv" AS row
                      OPTIONAL MATCH (character2:Character {id: row.character2})
                      WITH row where character2 is  null
                      return DISTINCT row.character2 AS missing""")

with open("data/characters_to_download.csv", "a") as characters_file:
    writer = csv.writer(characters_file, delimiter = ",")

    for row in rows:
        for row in rows:
            writer.writerow([row["missing"], ""])
