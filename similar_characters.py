from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.metrics.pairwise import cosine_similarity

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""
    MATCH (c:Character), (e:Episode)
    OPTIONAL MATCH (c)-[appearance:APPEARED_IN]->(e)
    RETURN e, c, appearance
    ORDER BY e.id, c.id""")

characters = {}
for row in rows:
    if characters.get(row["c"]["id"]) is None:
        if row["appearance"] is None:
            characters[row["c"]["id"]] = [0]
        else:
            characters[row["c"]["id"]] = [1]
    else:
        if row["appearance"] is None:
            characters[row["c"]["id"]].append(0)
        else:
            characters[row["c"]["id"]].append(1)

all = characters.values()

character_mapping = {}
for idx, character_id in enumerate(characters):
    character_mapping[idx] = character_id

for idx, character_id in enumerate(characters):
    similarity_matrix = cosine_similarity(all[idx:idx+1], all)[0]
    for other_idx, similarity_score in enumerate(similarity_matrix):
        other_character_id = character_mapping[other_idx]
        if character_id != other_character_id and similarity_score > 0:
            print character_id, other_character_id, similarity_score
            session.run("""
            MATCH (character1:Character {id: {character1}}), (character2:Character {id: {character2}})
            MERGE (character1)-[similarity:SIMILAR_TO]-(character2)
            ON CREATE SET similarity.score = {similarityScore}
            """, {'character1': character_id, 'character2': other_character_id, 'similarityScore': similarity_score})

session.close()
