import json
from database import GraphDB, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

with open("synthetic_data.json") as f:
    data = json.load(f)

db = GraphDB(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
db.load_data(data)
print("Data loaded into Neo4j successfully!")
db.close()