CREATE CONSTRAINT ON (e:Episode)
ASSERT e._id IS UNIQUE;

// Episodes
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mneedham/neo4j-got/master/data/import/overview.csv" AS row
WITH toint(row.season) AS season, toint(row.episode) as episode, row
MERGE (e:Episode {_id: season + "." + episode})
ON CREATE SET e.season = season, e.episode = episode, e.title = row.title;

// Characters
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mneedham/neo4j-got/master/data/import/characters.csv" AS row
WITH toint(row.season) AS season, toint(row.episode) as episode, row
WITH season + "." + episode AS id, row
MATCH (e:Episode {_id: id})
MERGE (a:Actor {name: row.actor})
MERGE (c:Character {name: row.character})
MERGE (a)-[:PLAYS]->(c)
MERGE (c)-[:APPEARS_IN]->(e)
