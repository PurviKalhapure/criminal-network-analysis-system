import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class GraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, data):
        with self.driver.session() as session:
            for person in data["people"]:
                session.run(
                    """
                    MERGE (p:Person {id: $id})
                    SET p.name = $name, p.phone = $phone,
                        p.address = $address, p.risk_flag = $risk_flag
                    """, **person
                )
            for rel in data["relationships"]:
                rel_clean = {k: (v if v is not None else 0) for k, v in rel.items()}
                session.run(
                    f"""
                    MATCH (a:Person {{id: $source}}), (b:Person {{id: $target}})
                    MERGE (a)-[r:{rel_clean['type']} {{
                        timestamp: $timestamp, amount: $amount, location: $location
                    }}]->(b)
                    """, **rel_clean
                )

    def get_network(self, person_id, hops=2):
        with self.driver.session() as session:
            result = session.run(
                f"""
                MATCH path = (p:Person {{id: $id}})-[*1..{hops}]-(connected)
                RETURN path
                """, id=person_id
            )
            return [record["path"] for record in result]