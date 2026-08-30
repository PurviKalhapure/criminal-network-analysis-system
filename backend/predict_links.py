import torch
import networkx as nx
from database import GraphDB, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from analytics import build_networkx_graph

db = GraphDB(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
G = build_networkx_graph(db.driver)

preds = nx.jaccard_coefficient(G)
predictions = [(u, v, p) for u, v, p in preds if p > 0]
top_predictions = sorted(predictions, key=lambda x: -x[2])[:10]

print("Top 10 predicted hidden connections (people not directly linked, but share many common associates):")
for u, v, score in top_predictions:
    print(f"  {u} <-> {v}  (similarity score: {score:.3f})")

db.close()