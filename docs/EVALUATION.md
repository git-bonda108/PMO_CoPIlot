# Evaluation

An honest account of how this system is tested today, what the code visibly handles, and the harness it should have.

## What exists

**There is no automated test suite.** No `tests/` directory, no pytest/unittest files, no CI configuration exists in the repository.

What does exist:

- **Manual QA catalog** — `PMO_COPILOT_TEST_CASES.md` defines 20 manual test cases (TC-001 … TC-020) covering agent outputs, UI tabs, charts, upload, EVM math, and the mode toggle, each with steps, expected output, and pass criteria as unchecked checklists. Note that several of its illustrative data snippets (e.g. lowercase `bac`/`ev` keys, `severity`/`age_days` fields) describe a schema that differs from the actual `mock_jira_data.py` structures.
- **Smoke entry points** — three modules are directly runnable as sanity checks:
  - `python evm_calculator.py` prints a full EVM report for a sample dataset;
  - `python mock_jira_data.py` prints the portfolio summary;
  - `python pmo_tools.py` prints the portfolio overview.
- **Determinism aids** — all ML training uses fixed seeds (`np.random.seed(42…46)`), and the burn-down chart uses `random.seed(42)`, so outputs are reproducible run to run.

No accuracy, latency, or quality metrics are measured anywhere in the code. (The performance and confidence figures in `PMO_COPILOT_FEATURES_WORKFLOW.md` are illustrative/simulated, as that document itself notes; the "confidence" values shown in the UI are computed by fixed formulas such as `70 + percent_complete * 0.25`, not measured model confidence.)

## Edge cases the code visibly handles

Enumerated from the source, with locations:

| Edge case | Handling | Where |
|-----------|----------|-------|
| Division by zero in EVM | CPI/SPI default to 0; EAC falls back to `BAC * 2`; TCPI to `inf`; percent fields to 0 | `evm_calculator.calculate_evm` |
| Unknown project key | Friendly "not found" message listing valid keys | every lookup in `pmo_tools.py` |
| Missing EVM block | "No EVM data available" message | `calculate_project_evm` |
| No blockers / no risks | Explicit empty-state messages | `get_project_blockers`, `get_workflow_status` |
| Sprints without velocity (planned/blocked) | Filtered out before averaging; trend needs ≥ 2 points | `get_sprint_status`, `get_schedule_analysis` |
| scikit-learn absent | `ML_AVAILABLE=False`; every model falls back to closed-form formulas | `ml_models.py` import guard + each `predict()` |
| XGBoost absent | GradientBoosting substitutes transparently | each XGBoost-based model |
| `ml_models` import failure | Tool returns a warning string instead of raising | `pmo_tools.get_ml_predictions` |
| Live API failure | Caught, warned, and rerouted to demo mode | `pmo_copilot_app.get_ai_response` |
| ML tool raising in demo mode | Caught; canned demo predictions substituted | `demo_runner._ml_predictions_agent` |
| Unparseable milestone dates in Gantt build | try/except skips the row | `pmo_copilot_app.py` (tab 6) |
| Prediction blow-ups | Outputs clamped (cost multiplier 0.8–2.0, delay −30…180 d, FTEs 2–25, probability 5–95%) | `ml_models.py`, `pmo_tools.get_predictive_analytics` |
| Unrecognized chat query | Help card with command list | `demo_runner._default_response` |

Not handled: no timeouts or retries around the OpenAI call (`tenacity` is installed but unused), no input-size limits on uploads, no guard on handoff chain length beyond SDK defaults.

## Known defects (checkable against the code)

These are factual mismatches a test harness would catch; they are documented here rather than fixed because this change set is documentation-only.

1. **Feature extractor key-case mismatch.** `EVMFeatureExtractor.extract_features` reads `evm.get('bac'/'ev'/'pv'/'ac')` (lowercase), but `mock_jira_data.py` stores `BAC/PV/EV/AC` (uppercase). The extractor therefore always falls back to its built-in defaults (BAC 1,000,000, etc.), so ML predictions do not reflect the selected project's EVM data.
2. **Risk schema mismatch.** The extractor counts risks by `r.get('severity')`, but the dataset uses `probability`/`impact`. `risk_score` and `high_risks` are therefore always 0.
3. **Blocker status mismatch.** The extractor treats any blocker without `status == 'RESOLVED'` as active; dataset blockers have no `status` field, so all count as active (coincidentally correct for this dataset).
4. **`get_ml_predictions` KeyError.** It formats `project['name']`, but projects use `project_name`. The chat-path ML query only works because `demo_runner` catches the exception and substitutes canned output; the ML Predictions tab avoids the bug by calling `get_full_ml_prediction` directly.
5. **Label vs. estimator.** The "Linear Regression" schedule model actually fits `Ridge(alpha=1.0)`; "feature importance" charts render a hard-coded dictionary, not values from the fitted models.
6. **Agent-count drift.** Marketing copy says "13 agents"; `pmo_copilot_agents.py` defines 12 `Agent` objects (orchestrator + 11 specialists). The 13th sidebar entry, "ML Predictions", is a direct model pathway, not an SDK agent.
7. **Undeclared ML dependencies.** `scikit-learn` and `xgboost` are imported (with fallbacks) but absent from `requirements.txt`, so a fresh install silently runs the formula fallbacks.

## Proposed evaluation harness

No harness exists; this section is a design, clearly labeled as such.

### Layer 1 — deterministic unit tests (pytest)

- `evm_calculator`: golden values for the four shipped project datasets (e.g. DPLAT: CPI = 2,700,000/3,150,000 ≈ 0.857, SPI = 0.8, EAC = 5,250,000) plus zero-division cases (AC = 0, PV = 0, AC = BAC).
- `pmo_tools`: each of the 14 tools returns non-empty Markdown for valid keys and the correct message for invalid ones; date-dependent output tested with a frozen clock.
- `ml_models`: schema contract tests that would have caught defects 1–4 above — feed a real project dict through `extract_features` and assert the features differ from the defaults; assert `get_ml_predictions` does not raise.
- Demo router: table-driven mapping of query → expected handler (e.g. "evm DPLAT" → EVM agent, "milestone" → Milestone Guardian), guarding the keyword-priority order.

### Layer 2 — golden dataset for agent behavior

Shape: a JSONL file of ~50 cases, each `{query, expected_first_agent, expected_tools (subset), expected_facts (strings that must appear, e.g. "0.857"), forbidden_facts}`. Run in Live AI Mode against the recorded four-project portfolio; score routing accuracy (did the orchestrator hand off to the expected specialist — observable from the SDK run items), tool-call precision/recall, and fact faithfulness (every numeric claim in the answer must appear in some tool output — directly checkable because all numbers originate in `pmo_tools`).

### Layer 3 — gates and metrics

- **Gates (CI-blocking):** unit layer 100% pass; routing accuracy ≥ 90% on the golden set; fact-faithfulness violations = 0 (no number in an answer that no tool produced); demo and live paths agree on all deterministic figures.
- **Tracked metrics (non-blocking):** tokens and latency per query, handoff-chain length distribution, fallback-to-demo rate.
- **Regression policy:** golden set is versioned with the mock dataset; any change to `mock_jira_data.py` or agent instructions requires regenerating and re-reviewing expected facts.
