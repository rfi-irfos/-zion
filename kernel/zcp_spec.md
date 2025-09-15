# Zion Context Protocol (ZCP) v0.1

Purpose: add a ternary validator to any action. Binary flows stay; ZCP returns –1 | 0 | +1 with constraints.

Core objects
- Ternary Verdict: { verdict:-1|0|1, confidence:0..1, axes:{}, rationale:[] }
- Trinity Log: { string, number(ISO-8601), symbol }

Endpoints (HTTP) / Messages (WS)
- GET /capabilities -> {server,version,capabilities[],policies[],schema_hash}
- POST /handshake   -> session token + nonce
- POST /decide      -> input:{action{name,args},context,policy,trinity} -> output:{verdict,confidence,axes,constraints[],rationale[]}
- POST /log         -> append-only Trinity Log
- GET /witness      -> stream of trinity lines (SSE/WS)
- POST /prove       -> attach proofs (hashes/signatures), optional

Security
- Optional Ed25519 signing over message body
- Replay protection via server nonce + monotonic timestamps
- Append-only logs, periodic snapshots to /archive/
- 90/10 law: default to 0 (Tend) with constraints when uncertain

Compatibility
- MCP calls can wrap in { zcp_envelope:{policy, trinity} } and consult /decide before execution.
