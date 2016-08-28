from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn import metrics
from sklearn.decomposition import PCA, TruncatedSVD

import numpy as np
import pandas as pd
import seaborn as sns

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

episode_mapping = {}
for idx, episode_id in enumerate(episodes):
    episode_mapping[idx] = episode_id

n_components = 2
reducer = TruncatedSVD(n_components=n_components)
reducer.fit(all)
new_all = reducer.transform(all)
print("%d: Percentage explained: %s\n" % (n_components, reducer.explained_variance_ratio_.sum()))

df = pd.DataFrame(None)
df["episodeId"] =  [episode_mapping[idx] for idx, value in enumerate(all)]
df["season"] = [seasons[episode_mapping[idx]] for idx, value in enumerate(all)]
df["X coordinate"] = [x[0] for x in new_all]
df["Y coordinate"] = [x[1] for x in new_all]

markers_choice_list = ['o', 's', '^', '.', 'v', '<']
markers_list = [markers_choice_list[seasons[i] - 1] for i in df["episodeId"]]

sns.lmplot("X coordinate",
           "Y coordinate",
           hue="season",
           data=df,
           fit_reg=False,
        #    markers=markers_list,
           scatter_kws={"s": 150})
sns.set(font_scale=2)
sns.plt.title('Visualization of GoT episodes in a 2-dimensional space')
sns.plt.subplots_adjust(right=0.80, top=0.90, left=0.12, bottom=0.12)

sns.plt.show()
