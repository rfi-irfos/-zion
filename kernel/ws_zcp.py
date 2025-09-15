#!/usr/bin/env python3
# ws_zcp.py — minimal ZCP WebSocket server (v0.1)

import asyncio, json, os
from datetime import datetime, timezone
from websockets import serve

AXES = {"safety":0.9, "sovereignty":0.9, "ecology":0.7, "openness":1.0}
CAPS = {"server":"zion-node","version":"0.1",
        "capabilities":["validate","witness","log","prove"],
        "policies":["temple-clause","90-10"]}

LEDGER_PATH = os.path.join(os.path.dirname(__file__), "..", "ledger", f"ledger_{datetime.now().year}.jsonl")

def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")

async def handle(ws):
    async for raw in ws:
        try:
            msg = json.loads(raw)
        except Exception:
            await ws.send(json.dumps({"error":"invalid json"}))
            continue

        mtype = msg.get("type")

        if mtype == "capabilities":
            await ws.send(json.dumps(CAPS))
            continue

        if mtype == "decide":
            action = msg.get("action", {}).get("name","")
            rules  = (msg.get("policy") or {}).get("rules", [])
            verdict, constraints, rationale = 1, [], []

            if "write" in action and "temple-clause" not in rules:
                verdict = 0
                constraints += ["add LICENSE_C0.md (or keep C0 visible)", "append decision to ledger"]
                rationale.append("write okay with openness + transparency constraints")

            if "delete" in action:
                verdict = -1
                rationale.append("hard delete conflicts with archive/burial principle")

            await ws.send(json.dumps({
                "verdict": verdict,
                "confidence": 0.8,
                "axes": AXES,
                "constraints": constraints,
                "rationale": rationale
            }))
            continue

        if mtype == "log":
            entry = msg.get("entry")
            if not entry:
                await ws.send(json.dumps({"error":"missing entry"})); continue
            os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
            with open(LEDGER_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            await ws.send(json.dumps({"ok": True, "at": now_iso()}))
            continue

        await ws.send(json.dumps({"error":"unknown type"}))

async def main():
    port = int(os.environ.get("ZCP_PORT", "9137"))
    async with serve(handle, "0.0.0.0", port):
        print(f"ZCP WS server on :{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
