from database import GraphDB, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from analytics import build_networkx_graph, get_centrality_rankings, detect_communities

db = GraphDB(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
G = build_networkx_graph(db.driver)

print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

rankings = get_centrality_rankings(G)
print("\nTop 5 Hubs (most connections - possible kingpins):")
for person_id, score in rankings["hubs"][:5]:
    print(f"  {person_id}: {score:.3f}")

print("\nTop 5 Brokers (bridges between groups):")
for person_id, score in rankings["brokers"][:5]:
    print(f"  {person_id}: {score:.3f}")

communities = detect_communities(G)
print(f"\nFound {len(communities)} communities/clusters")
for i, c in enumerate(communities[:5]):
    print(f"  Community {i+1}: {len(c)} members")

db.close()