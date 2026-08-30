from hashchain import HashChain

chain = HashChain()

chain.add_record("ADD_PERSON", "Officer_Sharma", "Added suspect P114 to investigation")
chain.add_record("ADD_RELATIONSHIP", "Officer_Sharma", "Linked P114 to P120 via call records")
chain.add_record("FLAG_RISK", "System", "P114 flagged as high risk based on network analysis")

print("Chain has", len(chain.chain), "blocks")
valid, message = chain.verify_integrity()
print(f"Integrity check: {message}")

print("\n--- Now tampering with a record ---")
chain.chain[1]["details"] = "Tampered data - fake record"
valid, message = chain.verify_integrity()
print(f"Integrity check after tampering: {message}")