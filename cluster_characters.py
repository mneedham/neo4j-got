from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn import metrics

import numpy as np

def build_character_matrix(driver, minimum_appearances):
    session = driver.session()
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
    session.close()
    return characters

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

minimum_appearances = 0
characters = build_character_matrix(driver, minimum_appearances)

character_mapping = {}
for idx, character_id in enumerate(characters):
    character_mapping[idx] = character_id

all = np.array(characters.values())
# print "Minimum appearances: {0}".format(minimum_appearances)
# for n_clusters in range(2, 11):
#     km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
#     cluster_labels = km.fit_predict(all)
#     silhouette_avg = metrics.silhouette_score(all, cluster_labels, sample_size=1000)
#     sample_silhouette_values = metrics.silhouette_samples(all, cluster_labels)
#     print n_clusters, silhouette_avg

n_components = 2
reducer = TruncatedSVD(n_components=n_components)
reducer.fit(all)
new_all = reducer.transform(all)
print("%d: Percentage explained: %s\n" % (n_components, reducer.explained_variance_ratio_.sum()))

# for n_clusters in range(2, 11):
#     km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
#     cluster_labels = km.fit_predict(new_all)
#     silhouette_avg = metrics.silhouette_score(new_all, cluster_labels, sample_size=1000)
#     sample_silhouette_values = metrics.silhouette_samples(new_all, cluster_labels)
#     print n_clusters, silhouette_avg

n_clusters = 7
km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
cluster_labels = km.fit_predict(new_all)
