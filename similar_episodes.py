from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.metrics.pairwise import cosine_similarity

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""
    MATCH (c:Character), (e:Episode)
    OPTIONAL MATCH (c)-[appearance:APPEARED_IN]->(e)
    RETURN e, c, appearance
    ORDER BY e.id, c.id""")

episodes = {}
for row in rows:
    if episodes.get(row["e"]["id"]) is None:
        if row["appearance"] is None:
            episodes[row["e"]["id"]] = [0]
        else:
            episodes[row["e"]["id"]] = [1]
    else:
        if row["appearance"] is None:
            episodes[row["e"]["id"]].append(0)
        else:
            episodes[row["e"]["id"]].append(1)

all = episodes.values()

episode_mapping = {}
for idx, episode_id in enumerate(episodes):
    episode_mapping[idx] = episode_id

for idx, episode_id in enumerate(episodes):
    similarity_matrix = cosine_similarity(all[idx:idx+1], all)[0]
    for other_idx, similarity_score in enumerate(similarity_matrix):
        other_episode_id = episode_mapping[other_idx]
        print episode_id, other_episode_id, similarity_score
        if episode_id != other_episode_id:
            session.run("""
            MATCH (episode1:Episode {id: {episode1}}), (episode2:Episode {id: {episode2}})
            MERGE (episode1)-[similarity:SIMILAR_TO]-(episode2)
            ON CREATE SET similarity.score = {similarityScore}
            """, {'episode1': episode_id, 'episode2': other_episode_id, 'similarityScore': similarity_score})

session.close()
