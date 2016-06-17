CREATE CONSTRAINT ON (e:Episode)
ASSERT e.id IS UNIQUE;

// Episodes
LOAD CSV WITH HEADERS FROM "file:///overview.csv" AS row
WITH toint(row.season) AS season, toint(row.episode) as episode, toint(row.episodeId) AS episodeId, row
MERGE (e:Episode {id: episodeId})
ON CREATE SET e.season = season, e.episode = episode, e.title = row.title;

// Characters
LOAD CSV WITH HEADERS FROM "file:///characters.csv" AS row

WITH toint(row.episodeId) AS id, row
MATCH (e:Episode {id: id})
MERGE (actor:Actor {name: row.actor})
MERGE (c:Character {name: row.character})
MERGE (appearance:Appearance {id: row.character + "_" + id})
MERGE (actor)-[:PLAYS]->(c)
MERGE (c)-[:MAKES_APPEARANCE]->(appearance)
MERGE (appearance)-[:IN_EPISODE]->(e);

// Locations
load csv with headers from "file:///locations.csv" AS row
MATCH (actor:Actor {name: row.actor})-[:PLAYS]->(character)
MATCH (appearance:Appearance {id:character.name + "_" + row.episodeId })
MERGE (location:Location {id: row.locationId})
MERGE (appearance)-[:IN_LOCATION]->(location);
