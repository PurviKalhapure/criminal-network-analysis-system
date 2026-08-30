from database import GraphDB, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from analytics import build_networkx_graph
from explainability import explain_risk_score

db = GraphDB(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
G = build_networkx_graph(db.driver)

with db.driver.session() as session:
    result = session.run("MATCH (p:Person) RETURN p.id AS id, p.risk_flag AS risk_flag")
    risk_data = {record["id"]: record["risk_flag"] for record in result}

test_person = "P114"
explanation = explain_risk_score(test_person, G, risk_data)

print(f"Explanation for {test_person}:")
print(f"  Total connections: {explanation['total_connections']}")
print(f"  Reasons:")
for reason in explanation['risk_reasons']:
    print(f"    - {reason}")
print(f"  Flagged associates: {explanation['flagged_associates']}")

db.close()