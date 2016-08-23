from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn import metrics
import numpy as np

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""
MATCH (c:Character), (e:Episode)
OPTIONAL MATCH (c)-[appearance:APPEARED_IN]->(e)
RETURN e, c, appearance
ORDER BY e.id, c.id
""")

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

session.close()

all = episodes.values()

episode_mapping = {}
for idx, episode_id in enumerate(episodes):
    episode_mapping[idx] = episode_id

for number_of_clusters in range(2, 10):
    km = KMeans(n_clusters=number_of_clusters, init='k-means++', max_iter=100, n_init=1)
    km.fit(all)
    print number_of_clusters, metrics.silhouette_score(np.array(all), km.labels_, sample_size=1000)
