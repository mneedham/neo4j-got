from neo4j.v1 import GraphDatabase, basic_auth
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn import metrics

# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
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

all = np.array(episodes.values())

episode_mapping = {}
for idx, episode_id in enumerate(episodes):
    episode_mapping[idx] = episode_id

for n_clusters in range(2, len(all) - 1):
    km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
    cluster_labels = km.fit_predict(all)

    silhouette_avg = metrics.silhouette_score(all, cluster_labels, sample_size=1000)
    sample_silhouette_values = metrics.silhouette_samples(all, cluster_labels)

    print n_clusters, silhouette_avg

    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig.set_size_inches(18, 7)
    # ax1.set_xlim([-0.1, 1])
    # ax1.set_ylim([0, len(all) + (n_clusters + 1) * 10])
    #
    # y_lower = 10
    # for i in range(n_clusters):
    #     ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
    #     ith_cluster_silhouette_values.sort()
    #
    #     size_cluster_i = ith_cluster_silhouette_values.shape[0]
    #     y_upper = y_lower + size_cluster_i
    #
    #     color = cm.spectral(float(i) / n_clusters)
    #     ax1.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values,
    #                       facecolor=color, edgecolor=color, alpha=0.7)
    #
    #     # Label the silhouette plots with their cluster numbers at the middle
    #     ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    #
    #     # Compute the new y_lower for next plot
    #     y_lower = y_upper + 10  # 10 for the 0 samples
    #
    # ax1.set_title("The silhouette plot for the various clusters.")
    # ax1.set_xlabel("The silhouette coefficient values")
    # ax1.set_ylabel("Cluster label")
    #
    # # The vertical line for average silhoutte score of all the values
    # ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    #
    # ax1.set_yticks([])  # Clear the yaxis labels / ticks
    # ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    #
    # # 2nd Plot showing the actual clusters formed
    # colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    # ax2.scatter(all[:, 0], all[:, 1], marker='.', s=30, lw=0, alpha=0.7,c=colors)
    #
    # # Labeling the clusters
    # centers = km.cluster_centers_
    # # Draw white circles at cluster centers
    # ax2.scatter(centers[:, 0], centers[:, 1], marker='o', c="white", alpha=1, s=200)
    #
    # for i, c in enumerate(centers):
    #     ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50)
    #
    # ax2.set_title("The visualization of the clustered data.")
    # ax2.set_xlabel("Feature space for the 1st feature")
    # ax2.set_ylabel("Feature space for the 2nd feature")
    #
    # plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
    #               "with n_clusters = %d" % n_clusters),
    #              fontsize=14, fontweight='bold')
    #
    # plt.show()
