# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Enterprise Custom Policies — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Enterprise Custom Policies"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(USE_CASE)


packs = {"acme": ["zxco", "rivalcorp"]}

class CheckIn(BaseModel):
    tenant: str
    text: str

@app.post("/check")
def check(body: CheckIn):
    base = safety.check_input(body.text)
    if base.action != "allow":
        return {"action": base.action, "reason_code": base.reason_code, "precedence": "global_critical"}
    banned = packs.get(body.tenant, [])
    for b in banned:
        if b.lower() in body.text.lower():
            return {"action": "refuse", "reason_code": f"custom_ban:{b}", "precedence": "enterprise_pack"}
    return {"action": "allow", "reason_code": "ok"}
