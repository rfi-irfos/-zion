#!/usr/bin/env python3
# zcp_mcp_wrapper.py — consult ZCP before an MCP tool call

import json, urllib.request

ZCP = "http://localhost:8013/decide"

def consult_zcp(mcp_call: dict, policy_rules=None):
    payload = {
        "action": {"name": f"{mcp_call.get('tool','')}.{mcp_call.get('name','')}".strip("."),
                   "args": mcp_call.get("args", {})},
        "policy": {"rules": policy_rules or ["temple-clause"]}
    }
    req = urllib.request.Request(ZCP, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=3) as resp:
        return json.loads(resp.read().decode("utf-8"))

if __name__ == "__main__":
    print(consult_zcp({"tool":"filesystem","name":"write","args":{"path":"x","data":"y"}}))
