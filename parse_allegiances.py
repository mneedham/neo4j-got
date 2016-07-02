from neo4j.v1 import GraphDatabase, basic_auth
import csv

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""LOAD CSV WITH HEADERS FROM "file:///allegiances.csv" AS row
                      WITH row
                      WHERE (NOT tolower(row.houseName) CONTAINS "former") AND (NOT tolower(row.houseName) CONTAINS "until")
                      MATCH (character:Character {id: row.character})
                      MATCH (house:House {id: row.houseLink})
                      RETURN row
                   """)

with open("data/import/characters_houses.csv", "w") as characters_houses_file:
    writer = csv.writer(characters_houses_file, delimiter = ",")
    writer.writerow(["character", "house"])

    for row in rows:
        row = row["row"]
        writer.writerow([row["character"], row["houseLink"]])

rows = session.run("""LOAD CSV WITH HEADERS FROM "file:///allegiances.csv" AS row
                      WITH row
                      WITH row WHERE tolower(row.houseName) CONTAINS "former" OR tolower(row.houseName) CONTAINS "until"
                      MATCH (character:Character {id: row.character})
                      MATCH (house:House {id: row.houseLink})
                      RETURN row
                   """)

with open("data/import/characters_previous_houses.csv", "w") as characters_houses_file:
    writer = csv.writer(characters_houses_file, delimiter = ",")
    writer.writerow(["character", "house"])

    for row in rows:
        row = row["row"]
        writer.writerow([row["character"], row["houseLink"]])
