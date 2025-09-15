#!/usr/bin/env python3
# http_zcp.py — minimal HTTP JSON (no external deps)

import json, os
from wsgiref.simple_server import make_server
from datetime import datetime

AXES = {"safety":0.9, "sovereignty":0.9, "ecology":0.7, "openness":1.0}
CAPS = {"server":"zion-node","version":"0.1",
        "capabilities":["validate","witness","log","prove"],
        "policies":["temple-clause","90-10"]}
LEDGER = os.path.join(os.path.dirname(__file__), "..", "ledger", f"ledger_{datetime.now().year}.jsonl")

def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def app(environ, start_response):
    path = environ.get("PATH_INFO","/")
    method = environ.get("REQUEST_METHOD","GET")
    try:
        length = int(environ.get("CONTENT_LENGTH","0"))
    except:
        length = 0
    body = environ["wsgi.input"].read(length) if length else b"{}"

    if path == "/capabilities":
        start_response("200 OK",[("Content-Type","application/json")])
        return [json.dumps(CAPS).encode("utf-8")]

    if path == "/decide" and method == "POST":
        msg = json.loads(body or b"{}")
        action = (msg.get("action") or {}).get("name","")
        rules = (msg.get("policy") or {}).get("rules", [])
        verdict, constraints, rationale = 1, [], []
        if "write" in action and "temple-clause" not in rules:
            verdict = 0
            constraints += ["add LICENSE_C0.md","append decision to ledger"]
            rationale.append("write okay with transparency constraints")
        if "delete" in action:
            verdict = -1
            rationale.append("hard delete conflicts with burial principle")
        resp = {"verdict":verdict,"confidence":0.8,"axes":AXES,
                "constraints":constraints,"rationale":rationale}
        start_response("200 OK",[("Content-Type","application/json")])
        return [json.dumps(resp).encode("utf-8")]

    if path == "/log" and method == "POST":
        msg = json.loads(body or b"{}")
        entry = msg.get("entry")
        if not entry:
            start_response("400 Bad Request",[("Content-Type","application/json")])
            return [b'{"error":"missing entry"}']
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        start_response("200 OK",[("Content-Type","application/json")])
        return [json.dumps({"ok":True,"at":now_iso()}).encode("utf-8")]

    start_response("404 Not Found",[("Content-Type","application/json")])
    return [b'{"error":"not found"}']

if __name__ == "__main__":
    with make_server("", 8013, app) as httpd:
        print("ZCP HTTP server on :8013")
        httpd.serve_forever()
