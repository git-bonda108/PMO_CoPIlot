# Architecture

This document describes what is actually in the code, module by module, and the reasoning visible in it.

## Component map

| Module | Lines | Responsibility |
|--------|-------|----------------|
| `pmo_copilot_app.py` | ~2,180 | Streamlit UI: 8 tabs, sidebar agent picker, mode toggle, Plotly charts, report download. Chooses between the live agent path and the demo path per query. |
| `pmo_copilot_agents.py` | ~915 | Defines 12 OpenAI Agents SDK `Agent` objects: 1 orchestrator + 11 specialists, their instructions, tool lists, and the handoff graph. Exposes `run_pmo_copilot(user_input)`. |
| `pmo_tools.py` | ~690 | 14 plain-Python tool functions that read the mock portfolio and format Markdown reports. Shared verbatim by both execution paths. |
| `demo_runner.py` | ~700 | `PMOCoPilotDemo.process_query()` — keyword router that simulates agent behavior offline, including a scripted multi-step "handoff chain" narrative. |
| `evm_calculator.py` | ~240 | `EVMMetrics` dataclass, `calculate_evm()` (CV, SV, CPI, SPI, EAC, ETC, VAC, TCPI), report formatter, threshold-based insights. |
| `ml_models.py` | ~675 | `EVMFeatureExtractor` plus five model classes (cost, schedule, risk, resources, burn rate) as lazy singletons; synthetic training data; formula fallbacks. |
| `mock_jira_data.py` | ~310 | Four hard-coded projects (ECOM, MAPP, DPLAT, SECU) with sprints, issues, blockers, risks, teams, milestones, and EVM inputs; accessor helpers. |

The `.xlsx` and `.pdf` files at the repository root are sample exports and briefing artifacts. The UI's upload widget parses uploaded `.xlsx` into session state (`load_excel_to_json`), but nothing downstream reads that parsed data — reports always come from `mock_jira_data.py`.

## Data flow end to end

Live AI Mode (sidebar toggle, requires `OPENAI_API_KEY` starting with `sk-`):

1. `st.chat_input` or an agent button produces a query string.
2. `get_ai_response()` creates a fresh asyncio event loop and calls `Runner.run(orchestrator_agent, user_input)`.
3. The orchestrator either answers with its own three tools (`portfolio_overview`, `project_details`, `get_current_date`) or hands off to a specialist chosen from its 11 `handoff()` entries; its instructions include an explicit keyword-to-agent routing table.
4. The active specialist runs its tool loop over its subset of the 14 function tools; its instructions define numeric handoff triggers (e.g. "CPI < 0.9 → hand off to EVM Analyst Agent"), so control may chain laterally through the specialist mesh.
5. `result.final_output` is appended to `st.session_state.chat_history` and rendered as Markdown.
6. Any exception in the API path is caught and the query is rerouted to the demo path (`st.warning` plus fallback).

Demo Mode (default, and the only path for the Portfolio/EVM/Visualization/ML tabs regardless of toggle):

1. `PMOCoPilotDemo.process_query()` lowercases the query and matches keyword lists in priority order (schedule/resource/milestone/ML first, then status/risk/escalation/etc.).
2. `_extract_project()` scans for a project key or name fragment.
3. The matched `_*_agent()` method calls the same `pmo_tools` functions and appends canned "AI insight" text.
4. Queries containing "comprehensive", "handoff", etc. trigger `_comprehensive_handoff_analysis()`, which runs four tool calls in sequence and narrates them as a scripted handoff chain.

Both paths terminate in `pmo_tools.py`, which reads module-level dictionaries from `mock_jira_data.py` and returns Markdown strings. There is no database, file store, or network I/O in the data layer.

## Orchestration analysis: what is sequential, parallel, async — and why

- **Sequential by construction.** The Agents SDK handoff model transfers control; the receiving agent replaces the sender rather than being called as a subroutine. At most one agent is active per query, so a "chain of analysis" (Risk → EVM → Escalation) is a linear relay, not a fan-out. This is the correct reading of the code: handoffs are declared with `handoff(agent)` on `Agent.handoffs`, and no tool-as-agent composition or parallel runner appears anywhere.
- **The handoff graph is a mesh, not a tree.** After all 12 agents are constructed, `pmo_copilot_agents.py` assigns cross-handoffs: each analytical specialist can reach 3–5 peers (Risk → Escalation/Schedule/EVM/Resource/Milestone, EVM → Schedule/Escalation/Resource/Predictive/SteerCo, and so on). Two agents are deliberate sinks — RAG Reporter and SteerCo Prep declare no outgoing handoffs, per the comment "they are endpoints".
- **Async is minimal.** `Runner.run` is awaited inside `asyncio.run` (CLI) or a per-query `new_event_loop` (Streamlit, to bridge the sync UI thread). Nothing else is asynchronous; `aiohttp`/`asyncio-throttle` in requirements are unused.
- **Tool sharing over tool specialization.** All agents draw from one pool of 14 tools; specialization comes from instructions and tool subsets (4–8 tools each), not from separate tool implementations. This keeps the data layer single-sourced.

## State and context engineering

- **Per-query statelessness.** `run_pmo_copilot()` passes only the current user string to `Runner.run`; prior turns are never included. Multi-turn coherence in the chat panel is cosmetic (rendered from `st.session_state.chat_history`), not fed to the model.
- **Context is assembled by tools, bounded by data size.** Agent context grows only through tool outputs — pre-formatted Markdown tables over a fixed four-project dataset — so context length is naturally bounded. There is no summarization, truncation, or windowing logic, which is adequate at this dataset size and would need revisiting with real portfolio volumes.
- **Structured prompting.** Every agent instruction starts with the SDK's `RECOMMENDED_PROMPT_PREFIX` (handoff-awareness boilerplate) followed by a role definition, an output template (report sections, escalation format, RAG thresholds), and an explicit `HANDOFF TRIGGERS` block with numeric thresholds (CPI/SPI 0.9, TCPI 1.1/1.2, delivery probability 70%). Encoding routing policy as thresholds in prose is the system's main context-engineering device.
- **UI state.** `st.session_state` holds chat history, last report, selected agent, mode flag, and parsed uploads. It is per-browser-session and in-memory only.

## Analytics layer

- **EVM.** `calculate_evm()` computes the full standard metric set from four inputs (BAC, PV, EV, AC) with explicit division-by-zero guards (CPI/SPI default 0, EAC defaults to `BAC * 2` when CPI is 0, TCPI to `inf` when the remaining budget is 0). Health thresholds (1.0 / 0.9) are centralized in three small functions.
- **ML.** Five singleton models train lazily on first use, each on 500 synthetic samples generated from seeded `numpy.random` draws pushed through hand-written formulas (e.g. cost multiplier from 1/CPI plus risk and blocker terms, clamped to 0.8–2.0). Estimator choice degrades gracefully: XGBoost → scikit-learn `GradientBoosting*` → pure-formula fallback when scikit-learn itself is missing. The "Schedule Predictor" fits `Ridge(alpha=1.0)` although the UI labels it Linear Regression, and `get_feature_importance()` returns a hard-coded dictionary rather than reading the fitted models. Because training data is synthetic and derived from the same formulas the fallbacks use, the models are best understood as a demonstration of an ML pipeline shape, not as validated predictors — see docs/EVALUATION.md.

## Design decisions and trade-offs visible in the code

1. **Dual execution paths behind one tool layer.** The demo router duplicates the routing concern (keywords vs. LLM triage) but shares 100% of the data/formatting code, so demo output is representative of live output. Trade-off: routing logic exists twice and can drift.
2. **Handoff mesh over supervisor loop.** Specialists escalate to each other directly, which produces natural analysis chains without a central planner, at the cost of no global view of a multi-agent run and no guard against long relay chains beyond the SDK's own limits.
3. **Deterministic analytics under LLM narration.** All numbers (EVM, RAG thresholds, delivery probability) are computed in Python and handed to the model as text; the LLM formats and explains but does not compute. This keeps figures reproducible and cheap to verify.
4. **Read-only, in-process data.** Hard-coding the portfolio removes integration risk from the demo and makes every report reproducible; the upload widget sketches where a real ingestion path would attach.
5. **Fail-open to demo mode.** Any live-mode exception degrades to the offline path rather than surfacing an error page — the right bias for a demonstration system, the wrong one for production (see docs/HARDENING.md).

## Extending this system

Grounded next steps that the current structure makes cheap:

1. **Wire the upload path into the data layer.** `load_excel_to_json()` already parses Jira-style `.xlsx` into dictionaries; defining a mapping from those sheets to the `mock_jira_data` project schema (the de-facto data contract used by all 14 tools) would make every agent, chart, and report work on real exports without touching the agent layer.
2. **Fix and enforce the feature-extraction contract.** `EVMFeatureExtractor` expects lowercase `evm` keys and a `severity` field that the dataset does not provide (see EVALUATION). Normalizing the schema in one place — or validating it with the `pydantic` dependency already installed — would let the ML models actually see the portfolio data.
3. **Pass conversation history into `Runner.run`.** The chat UI already stores history; threading it into the run input would give the agents multi-turn context (follow-up questions like "and for MAPP?") with a small, localized change to `run_pmo_copilot()`.
4. **Replace synthetic training with recorded portfolio history.** The five model classes isolate `_generate_training_data()` behind a stable `predict()` interface, so substituting real historical snapshots is a data change, not an architecture change.
5. **Make routing policy testable.** The orchestrator's keyword table and the specialists' numeric handoff triggers are prose today. Extracting them into a declarative table shared by both the demo router and the agent instructions would eliminate the demo/live drift risk and give the evaluation harness (proposed in EVALUATION) a routing ground truth to assert against.
