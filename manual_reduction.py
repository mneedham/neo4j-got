from neo4j.v1 import GraphDatabase, basic_auth
from sklearn import metrics
from sklearn.cluster import KMeans

import numpy as np
import pandas as pd

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

for minimum_appearances in range(0, 20):
    rows = session.run("""
    MATCH (e:Episode)<-[:APPEARED_IN]-(c)
    WITH c, COUNT(*) AS apps
    WHERE apps > {minimumAppearances}
    WITH c
    MATCH (e:Episode)
    OPTIONAL MATCH (c)-[appearance:APPEARED_IN]->(e)
    RETURN e, c, appearance
    ORDER BY e.id, c.id
    """, {'minimumAppearances': minimum_appearances})

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

    all = np.array(episodes.values())

    print "Minimum appearances: {0}".format(minimum_appearances)
    for n_clusters in range(2, 10):
        km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
        cluster_labels = km.fit_predict(all)

        silhouette_avg = metrics.silhouette_score(all, cluster_labels, sample_size=1000)
        sample_silhouette_values = metrics.silhouette_samples(all, cluster_labels)

        print "\t", n_clusters, silhouette_avg

    session.close()
