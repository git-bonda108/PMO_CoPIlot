# Hardening

Current security and operational posture of the codebase, followed by a staged ladder to production. Grounded in what the code is today: a single-user Streamlit demo over an in-process mock dataset.

## Current posture

**Authentication and authorization**
- None. The Streamlit app binds to localhost:8501 with no login, no roles, and no per-user data separation. Anyone who can reach the port can use every agent and read all portfolio data.

**Secrets handling**
- API keys are read from environment variables via `python-dotenv`; `.env`, `.env.local`, and `.env.*.local` are gitignored, and no `.env` file is committed.
- A scan of every tracked file at HEAD (source, docs, and the binary `.xlsx`/`.pdf` artifacts) found no live credentials — the only key-shaped strings are placeholders in documentation (`sk-ant-...`, `your_openai_api_key`).
- The Live AI gate is a prefix check (`OPENAI_API_KEY` starts with `sk-`); the key itself is never logged or rendered.
- `ANTHROPIC_API_KEY` is read into a variable but unused; keeping unused secret plumbing around invites accidental scope creep and should be removed when code changes are next in scope.

**Input handling**
- Chat input goes to keyword matching (demo) or to the LLM (live). Prompt-injection resistance is not addressed; in live mode a crafted query could steer agent instructions. Blast radius is limited because all 14 tools are read-only over hard-coded data — there is no tool that writes, deletes, or calls external systems.
- The `.xlsx` upload is parsed with pandas/openpyxl with no size, sheet-count, or schema validation. Parsed data is stored in session state and currently unused downstream, which limits impact.
- The UI renders extensive `unsafe_allow_html=True` blocks. Today the interpolated values are trusted constants from the mock dataset; the moment uploaded or external data flows into those templates, this becomes an XSS vector.

**Error handling**
- Live-mode API failures fail open into demo mode with a truncated warning — good demo behavior, but it can mask outages and silently serve canned data where real analysis is expected.
- Broad `except` blocks (Gantt date parsing, demo ML path) swallow errors without logging.
- No timeouts or retries wrap the OpenAI call; `tenacity` is a declared dependency but is never used.

**Observability**
- No logging framework, no metrics, no tracing. The only diagnostics are `print` on agents-import failure and `st.warning` on API fallback. Agent runs (which specialist handled a query, which tools ran, token spend) are not recorded.

**Dependency posture**
- `requirements.txt` declares a substantially larger surface than the code uses (LangChain family, FAISS, ChromaDB, pypdf, python-docx, aiohttp, tenacity, rich are all unused), enlarging the supply-chain and CVE surface for no benefit. Conversely, `scikit-learn`/`xgboost` are used but undeclared. Versions are floors (`>=`) with no lockfile, so builds are not reproducible.

## Ladder to production

Each stage assumes the previous one is done.

### Stage 1 — Identity, keys, and dependency hygiene
- Put the app behind authentication: a reverse proxy with SSO (OIDC/SAML) in front of Streamlit, or an auth-capable hosting platform; add role separation if portfolio data becomes real (PM vs. executive views).
- Move keys from `.env` to a secrets manager appropriate to the deployment target; rotate on any suspicion; never bake keys into images.
- Prune `requirements.txt` to actual imports, add `scikit-learn`/`xgboost` explicitly, and pin with a lockfile (pip-tools or uv); add dependency and secret scanning (e.g. pip-audit, gitleaks) to CI.
- Remove the unused `ANTHROPIC_API_KEY` plumbing or implement the path that needs it.

### Stage 2 — Robustness and monitoring
- Wrap the OpenAI call with timeout, bounded retries (the installed `tenacity` fits), and a circuit breaker; make fallback-to-demo explicit in the UI ("showing offline data") rather than silent.
- Replace bare `except` with logged, typed handling; adopt structured logging (JSON) with per-query correlation IDs.
- Record agent-run telemetry: chosen specialist, handoff chain, tool calls, token counts, latency — the Agents SDK exposes run items suitable for this. Alert on error rate and fallback rate.
- Validate uploads (size cap, sheet whitelist, schema check with the already-installed `pydantic`) before parsing; escape or drop `unsafe_allow_html` rendering for any non-constant data.
- Add the evaluation harness from docs/EVALUATION.md to CI as a quality gate.

### Stage 3 — Deployment
- Containerize with a slim, non-root image; run Streamlit behind TLS on a reverse proxy; set resource limits.
- Externalize state: real portfolio data belongs in a database or an actual Jira integration with least-privilege API scopes, not in-process dictionaries; session state should survive restarts if multi-turn features land.
- Separate environments (dev/staging/prod) with distinct keys and budgets; cap LLM spend per environment and per user.
- CI/CD: lint, tests, eval gates, image scan, then deploy; keep rollback to the previous image one step.

### Stage 4 — Compliance and data governance
- Once real project data flows in, classify it (portfolio financials and staffing data are typically internal-confidential) and document what is sent to the LLM provider; obtain data-processing terms accordingly, or route through an enterprise endpoint with no-training guarantees.
- Retention: define how long chat history, uploads, and telemetry are kept; provide deletion.
- Access reviews and audit logs for who queried what, mapped to the Stage 1 identity layer.
- If the product's own SOC 2-style claims matter (the mock portfolio itself models a compliance project), the Stage 2 logging and Stage 3 environment separation are the evidence base an auditor will ask for.

## Secrets found at HEAD

None. No credentials required redaction or removal; `.gitignore` already excludes `.env` variants. Documentation examples use placeholders only.
