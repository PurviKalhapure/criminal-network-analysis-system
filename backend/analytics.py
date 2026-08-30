import networkx as nx

def build_networkx_graph(driver):
    G = nx.Graph()
    with driver.session() as session:
        result = session.run("MATCH (a:Person)-[r]->(b:Person) RETURN a.id AS source, b.id AS target")
        for record in result:
            G.add_edge(record["source"], record["target"])
    return G

def get_centrality_rankings(G):
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    top_hubs = sorted(degree.items(), key=lambda x: -x[1])[:10]
    top_brokers = sorted(betweenness.items(), key=lambda x: -x[1])[:10]
    return {"hubs": top_hubs, "brokers": top_brokers}

def detect_communities(G):
    from networkx.algorithms.community import louvain_communities
    communities = louvain_communities(G)
    return [list(c) for c in communities]