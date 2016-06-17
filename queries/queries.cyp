// Find everyone who was in Braavos
match (location:Location {id: "In_Braavos"})<-[r:IN_LOCATION]-(app)<-[r1:MAKES_APPEARANCE]-(character),
      (app)-[r2:IN_EPISODE]->(episode)
RETURN *
