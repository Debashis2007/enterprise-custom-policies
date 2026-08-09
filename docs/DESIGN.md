# Design: Enterprise Custom Policies

**Project:** `enterprise-custom-policies`  
**Parent system design:** `06-safety-moderation-pipeline.md`

## 1. What this POC demonstrates

Global critical policy plus per-tenant packs; custom packs cannot weaken global critical.

## 2. Architecture (POC)

```text
check → global SafetyPlane first → tenant ban list → allow/refuse
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Policy-as-data packs | Enterprises need custom rules without forks. | `packs[tenant]`. |
| Precedence: global critical wins | Custom allow must never bypass critical. | Global check first. |
| Custom reason codes | Admins need to see which pack rule fired. | `custom_ban:…`. |

## 4. Key endpoints

`GET /health`, `POST /check`

## 5. Tradeoffs / POC limits

No shadow-mode pack canary in this stub.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

