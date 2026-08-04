# JavaScript Standards (YepCode / Factorial Code)

JavaScript is the secondary language. Runtime: **Node 20 on YepCode**, **Node 22 on Factorial Code**. Use it when a project or an existing App is already JS, or when a required SDK is JS-only; otherwise default to Python.

All structural rules from `python-standards.md` apply unchanged: project layout, layering, module vs process naming, datastore key rules, config/secrets, state, webhooks, logging discipline. This file covers only the JS-specific deltas.

## 1. Process entrypoint

Wrap all logic in `main()` and export it (required for debugging and tests). Top-level `await` is allowed (code runs inside an async wrapper), but keep logic in `main()` anyway.

```javascript
// processes/<slug>/main.js  (index.js on YepCode)
const { fcode } = require('fcode');   // YepCode: global `yepcode`, no require

async function main() {
  const params = fcode.context.parameters;
  const orchestrator = fcode.import('sync_orchestrator');
  const result = await orchestrator.run(params);
  return { status: 200, body: result };
}

module.exports = { main };
main();
```

- Modules use CommonJS (`module.exports`) and are imported with `fcode.import("name")` / `yepcode.import("name")` — **literal strings only**.
- The execution waits for all pending promises; never leave dangling promises intentionally.

## 2. Dependencies

- Prefer built-ins (`fetch` is native on Node 20+). Declare third-party deps pinned via `// @add-package pkg=x.y.z` (e.g. `// @add-package openai=4.79.1`) or the team `package.json` manifest.
- Factorial API on Factorial Code: `FactorialClient` from `base-app`, backed by `@factorialco/api-client`. Never hand-roll Factorial calls.

## 3. Style

- `async/await` only — no raw promise chains, no callbacks.
- `const` by default; no `var`.
- JSDoc type annotations on public functions (no TypeScript compiler on-platform; JSDoc keeps editor type-checking).
- Errors: custom error classes at client boundaries, same mapping discipline as Python.
- Built-in email on Factorial Code: `fcode.sendMail` (max 3 per execution).
