import hashlib
import json
import time

class HashChain:
    def __init__(self):
        self.chain = []
        self._add_genesis_block()

    def _add_genesis_block(self):
        genesis = {"index": 0, "timestamp": time.time(), "data": "GENESIS", "previous_hash": "0"}
        genesis["hash"] = self._compute_hash(genesis)
        self.chain.append(genesis)

    def _compute_hash(self, block):
        block_string = json.dumps(
            {k: v for k, v in block.items() if k != "hash"}, sort_keys=True
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_record(self, action, actor, details):
        previous_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "action": action,
            "actor": actor,
            "details": details,
            "previous_hash": previous_block["hash"]
        }
        new_block["hash"] = self._compute_hash(new_block)
        self.chain.append(new_block)
        return new_block

    def verify_integrity(self):
        for i in range(1, len(self.chain)):
            current, previous = self.chain[i], self.chain[i - 1]
            if current["previous_hash"] != previous["hash"]:
                return False, f"Tampering detected at block {i}"
            if self._compute_hash(current) != current["hash"]:
                return False, f"Block {i} has been altered"
        return True, "Chain intact — no tampering detected"