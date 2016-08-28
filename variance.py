# import numpy as np
# from sklearn.decomposition import PCA
#
# np.random.seed(0)
# my_matrix = np.random.randn(20, 5)
#
# my_model = PCA(n_components=5)
# my_model.fit_transform(my_matrix)
#
# print my_model.explained_variance_
# print my_model.explained_variance_ratio_
# print my_model.explained_variance_ratio_.cumsum()

from neo4j.v1 import GraphDatabase, basic_auth
from sklearn import metrics
from sklearn.decomposition import PCA, TruncatedSVD

import numpy as np
import pandas as pd

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))
session = driver.session()

rows = session.run("""
MATCH (e:Episode)<-[:APPEARED_IN]-(c)
WITH c, COUNT(*) AS apps
WHERE apps > 1
WITH c
MATCH (e:Episode)
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

my_model = PCA(n_components = 200)
my_model.fit_transform(all)

print my_model.explained_variance_
print my_model.explained_variance_ratio_
print my_model.explained_variance_ratio_.cumsum()
