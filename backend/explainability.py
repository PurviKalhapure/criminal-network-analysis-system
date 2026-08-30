def explain_risk_score(person_id, G, risk_data):
    if person_id not in G:
        return {"person_id": person_id, "risk_reasons": ["Person not found in network"], "flagged_associates": []}

    neighbors = list(G.neighbors(person_id))
    flagged_neighbors = [n for n in neighbors if risk_data.get(n, False)]

    reasons = []
    if len(flagged_neighbors) > 0:
        reasons.append(f"{len(flagged_neighbors)} direct associate(s) already flagged with prior records")
    if len(neighbors) > 15:
        reasons.append(f"unusually high number of connections ({len(neighbors)}) — possible hub/broker role in network")
    if len(neighbors) == 0:
        reasons.append("isolated node with no connections")

    if not reasons:
        reasons.append("no strong individual risk indicators found based on current network position")

    return {
        "person_id": person_id,
        "total_connections": len(neighbors),
        "risk_reasons": reasons,
        "flagged_associates": flagged_neighbors
    }