# minimal ZCP WebSocket skeleton (pseudocode)
import json, time, hashlib
from websockets import serve

def decide(payload):
    # naive evaluator: apply temple-clause + openness
    action = payload["action"]["name"]
    axes = {"safety":0.9, "sovereignty":0.9, "ecology":0.7, "openness":1.0}
    verdict, constraints, rationale = 1, [], []
    if "write" in action and not payload["policy"]["rules"]:
        verdict = 0
        constraints.append("add LICENSE_C0.md and log to ledger")
        rationale.append("write allowed with openness + transparency")
    return {
        "verdict": verdict,
        "confidence": 0.8,
        "axes": axes,
        "constraints": constraints,
        "rationale": rationale
    }

async def handler(ws):
    async for raw in ws:
        msg = json.loads(raw)
        if msg.get("type") == "decide":
            await ws.send(json.dumps(decide(msg)))
        elif msg.get("type") == "capabilities":
            await ws.send(json.dumps({
                "server":"zion-node","version":"0.1",
                "capabilities":["validate","witness","log","prove"],
                "policies":["temple-clause","90-10"]
            }))
        # append-only logging etc.

async def main():
    async with serve(handler, "0.0.0.0", 9137):
        await asyncio.Future()

# run main()
