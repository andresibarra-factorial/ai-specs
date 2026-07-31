---
name: factorial-oas
description: Use when work involves the Factorial API - starting a new project, designing or implementing against endpoints, verifying fields/schemas/auth, or checking whether the project's pinned API version has drifted from the latest available OAS snapshot.
---

# Factorial OAS

Locate, query, and version-check the Factorial OpenAPI spec. Never answer Factorial API questions from memory — always from the file.

## Locate

1. Search for `factorial-oas-*.json` in the project, then in sibling/parent folders and session uploads. Naming: `factorial-oas-YYYY-MM-DD.json`, where the date **is** the API version. Newest date = latest snapshot.
2. If none found, ask the user for it (Factorial publishes a new snapshot ~every 3 months).

## Query (never read the whole file — ~1MB, ~380 paths)

Use `jq` or Python:

```bash
jq -r '.info.version' <oas>                                        # version
jq -r '.paths | keys[]' <oas> | grep -i <resource>                 # find endpoints
jq '.paths["/api/<ver>/resources/<domain>/<res>"]' <oas>           # operations, params
jq '.components.schemas["<Name>"]' <oas>                           # schema
jq -r '[.paths[][].tags[]] | unique[]' <oas>                       # Domain > Resource tags
jq '.components.securitySchemes' <oas>                             # auth (apikey x-api-key, oauth2)
```

URL pattern: `{base}/api/{version}/resources/{domain}/{resource}`. Tags (`Domain > Resource`) are the real grouping.

## Version drift check

Compare the project's pinned version (build brief §2 / config module) with the newest snapshot's version. If they differ, report: pinned vs latest, endpoints the project uses that changed (diff those paths/schemas between snapshots when both files are available), and a recommendation — but **the user decides** whether to bump the pin. Record the outcome in the build brief.

## Answer format

Always cite: OAS file used, its version, and the exact path/schema queried. If an endpoint or field is absent from the spec, say so explicitly — do not guess a similar one.
