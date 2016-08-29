import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.manifold import TSNE
from numpy.random import rand

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

all = np.array(characters.values())

character_mapping = {}
for idx, character_id in enumerate(characters):
    character_mapping[idx] = character_id

model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
new_all =  model.fit_transform(all)

df = pd.DataFrame(None)
df["characterId"] =  [character_mapping[idx] for idx, value in enumerate(all)]
df["X coordinate"] = [x[0] for x in new_all]
df["Y coordinate"] = [x[1] for x in new_all]

# sns.lmplot("X coordinate",
#            "Y coordinate",
#            data=df,
#            fit_reg=False,
#            scatter_kws={"s": 150})
# sns.set(font_scale=2)
# sns.plt.title('Visualization of GoT characters')
# sns.plt.subplots_adjust(right=0.80, top=0.90, left=0.12, bottom=0.12)
#
# sns.plt.show()

def onpick3(event):
    ind = event.ind
    print "ind:{0}, x:{1}, y:{2}, id: {3}".format(ind, df["X coordinate"][ind], df["Y coordinate"][ind], df["characterId"][ind])

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(df["X coordinate"], df["Y coordinate"], picker = True)

fig.canvas.mpl_connect('pick_event', onpick3)
plt.show()

# x, y, c, s = rand(4, 100)
# def onpick3(event):
#     ind = event.ind
#     print 'onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind)
#
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# col = ax1.scatter(x, y, 100*s, c, picker=True)
# #fig.savefig('pscoll.eps')
# fig.canvas.mpl_connect('pick_event', onpick3)
#
# plt.show()
