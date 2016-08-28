from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn import metrics
from sklearn.decomposition import PCA, TruncatedSVD

import numpy as np
import pandas as pd

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""
MATCH (c:Character), (e:Episode)
OPTIONAL MATCH (c)-[appearance:APPEARED_IN]->(e)
RETURN e, c, appearance
ORDER BY e.id, c.id
""")

episodes = {}
seasons = {}

for row in rows:
    seasons[row["e"]["id"]] = row["e"]["season"]

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

all = np.array(episodes.values())

for n_components in range(2, 30):
    reducer = TruncatedSVD(n_components=n_components)
    reducer.fit(all)
    new_all = reducer.transform(all)
    print("%d: Percentage explained: %s\n" % (n_components, reducer.explained_variance_ratio_.sum()))

    for n_clusters in range(2, 10):
        km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
        cluster_labels = km.fit_predict(new_all)

        silhouette_avg = metrics.silhouette_score(new_all, cluster_labels, sample_size=1000)
        sample_silhouette_values = metrics.silhouette_samples(new_all, cluster_labels)

        print "--", n_clusters, silhouette_avg
