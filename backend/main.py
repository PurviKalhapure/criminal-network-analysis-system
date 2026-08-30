from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx

from database import GraphDB, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from analytics import build_networkx_graph, get_centrality_rankings, detect_communities
from explainability import explain_risk_score
from hashchain import HashChain

app = FastAPI(title="Criminal Network Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = GraphDB(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
evidence_chain = HashChain()


def get_risk_data():
    with db.driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p.id AS id, p.risk_flag AS risk_flag")
        return {record["id"]: record["risk_flag"] for record in result}


@app.get("/")
def root():
    return {"message": "Criminal Network Analysis API is running"}


@app.get("/network/{person_id}")
def get_network(person_id: str, hops: int = 2):
    with db.driver.session() as session:
        result = session.run(
            f"""
            MATCH (p:Person {{id: $id}})-[r*1..{hops}]-(connected)
            RETURN p, r, connected
            """, id=person_id
        )
        nodes = {}
        edges = []
        for record in result:
            for node in [record["p"], record["connected"]]:
                nodes[node["id"]] = dict(node)
            for rel in record["r"]:
                edges.append({
                    "source": rel.start_node["id"],
                    "target": rel.end_node["id"],
                    "type": rel.type
                })
        return {"nodes": list(nodes.values()), "edges": edges}


@app.get("/analytics/centrality")
def centrality():
    G = build_networkx_graph(db.driver)
    return get_centrality_rankings(G)


@app.get("/analytics/communities")
def communities():
    G = build_networkx_graph(db.driver)
    return {"communities": detect_communities(G)}


@app.get("/analytics/hidden-links")
def hidden_links():
    G = build_networkx_graph(db.driver)
    preds = nx.jaccard_coefficient(G)
    predictions = [(u, v, p) for u, v, p in preds if p > 0]
    top = sorted(predictions, key=lambda x: -x[2])[:10]
    return {"predictions": [{"person_a": u, "person_b": v, "score": round(p, 3)} for u, v, p in top]}


@app.get("/explain/{person_id}")
def explain(person_id: str):
    G = build_networkx_graph(db.driver)
    risk_data = get_risk_data()
    return explain_risk_score(person_id, G, risk_data)


@app.post("/log-action")
def log_action(action: str, actor: str, details: str):
    block = evidence_chain.add_record(action, actor, details)
    return block


@app.get("/verify-chain")
def verify_chain():
    valid, message = evidence_chain.verify_integrity()
    return {"valid": valid, "message": message}


@app.get("/all-people")
def all_people():
    with db.driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p.id AS id, p.name AS name, p.risk_flag AS risk_flag")
        return {"people": [dict(record) for record in result]}