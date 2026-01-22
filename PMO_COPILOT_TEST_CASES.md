# PMO CoPilot - Test Cases Documentation

## 📋 Overview

This document provides comprehensive test cases for each feature of PMO CoPilot, including test data, expected outputs, and background processes.

---

## 🧪 Test Case Categories

1. [Agent Functionality Tests](#agent-functionality-tests)
2. [UI Component Tests](#ui-component-tests)
3. [ML Prediction Tests](#ml-prediction-tests)
4. [Visualization Tests](#visualization-tests)
5. [Data Processing Tests](#data-processing-tests)
6. [Integration Tests](#integration-tests)

---

## Agent Functionality Tests

### TC-001: Status Report Agent

| Field | Value |
|-------|-------|
| **Test ID** | TC-001 |
| **Feature** | Status Report Agent |
| **Priority** | High |

**Test Data:**
- Project: DPLAT (Data Platform Modernization)
- Data source: `mock_jira_data.py`

**Test Steps:**
1. Click "Status Report Agent" in sidebar
2. Observe the Generated Report section

**Expected Output:**
```
# 📊 Status Report Agent

Generated: [Current Date Time]

## Portfolio Status Report
### DPLAT - Data Platform Modernization
- Status: 🔴 RED
- Health: Critical
- Sprint: Sprint 5
- Progress: ~70% complete

### Key Metrics
- Issues: [X] Stories, [Y] Bugs, [Z] Tasks
- Velocity: [Value] points/sprint
```

**Background Process:**
1. `st.session_state.demo.process_query("status DPLAT")` called
2. `_status_report_agent()` method invoked
3. `get_portfolio_overview()` from `pmo_tools.py` fetches data
4. `ALL_PROJECTS['DPLAT']` data retrieved
5. Report formatted with Markdown
6. `st.session_state.last_report` updated
7. `st.rerun()` triggers UI refresh

**Pass Criteria:**
- [ ] Report displays within 2 seconds
- [ ] Correct project data shown
- [ ] RAG status accurate
- [ ] No errors in console

---

### TC-002: Risk Prediction Agent

| Field | Value |
|-------|-------|
| **Test ID** | TC-002 |
| **Feature** | Risk Prediction Agent |
| **Priority** | High |

**Test Data:**
```python
# From mock_jira_data.py
DPLAT_PROJECT = {
    'risks': [
        {'id': 'RISK-1', 'severity': 'HIGH', 'probability': 0.8},
        {'id': 'RISK-2', 'severity': 'MEDIUM', 'probability': 0.5}
    ]
}
```

**Test Steps:**
1. Click "Risk Prediction Agent" in sidebar
2. Or type "risks" in chat input

**Expected Output:**
```
# ⚠️ Risk Prediction Agent

## Active Risks Analysis
### DPLAT - Data Platform Modernization
| Risk | Severity | Probability | Impact |
|------|----------|-------------|--------|
| Legacy system dependencies | 🔴 HIGH | 80% | Schedule delay |
| Resource constraints | 🟡 MEDIUM | 50% | Budget overrun |

### AI Risk Prediction
- Delay Probability: 85%
- Budget Overrun Risk: HIGH
```

**Background Process:**
1. `process_query("risks")` routes to `_risk_prediction_agent()`
2. `get_project_risks()` from `pmo_tools.py` called
3. Risk data aggregated from all projects
4. AI predictions calculated based on:
   - CPI/SPI values
   - Number of high-severity risks
   - Blocker count and age
5. Report formatted and displayed

**Pass Criteria:**
- [ ] All risks from data source displayed
- [ ] Severity colors correct (🔴 HIGH, 🟡 MEDIUM, 🟢 LOW)
- [ ] AI predictions section present
- [ ] Handoff recommendations shown for critical risks

---

### TC-003: Escalation Agent

| Field | Value |
|-------|-------|
| **Test ID** | TC-003 |
| **Feature** | Escalation Agent |
| **Priority** | High |

**Test Data:**
```python
DPLAT_BLOCKERS = [
    {'id': 'BLOCK-1', 'age_days': 8, 'status': 'OPEN'},
    {'id': 'BLOCK-2', 'age_days': 15, 'status': 'OPEN'}
]
```

**Test Steps:**
1. Type "escalate DPLAT" in chat
2. Or click "Escalation Agent" and select DPLAT

**Expected Output:**
```
# 🚨 Escalation Agent

## URGENT: DPLAT Requires Immediate Attention

### Critical Blockers (8+ days)
| Blocker | Age | Impact | Stakeholder |
|---------|-----|--------|-------------|
| Legacy API migration | 15 days | Critical Path | VP Engineering |
| Database credentials | 8 days | Team blocked | IT Security |

### Escalation Actions Required
1. Schedule emergency meeting with stakeholders
2. Assign additional resources
3. Consider timeline adjustment
```

**Background Process:**
1. `process_query("escalate DPLAT")` called
2. `_escalation_agent("DPLAT")` invoked
3. `generate_escalation_report("DPLAT")` from `pmo_tools.py`
4. Blockers filtered for age > 5 days
5. EVM metrics checked (CPI/SPI < 0.9 triggers escalation)
6. Stakeholder matrix consulted
7. Priority determined based on:
   - Blocker age
   - Project criticality
   - EVM health indicators

**Pass Criteria:**
- [ ] Only blockers > 5 days shown in critical section
- [ ] Correct stakeholder assignments
- [ ] Action items relevant to issues
- [ ] URGENT label for critical projects

---

### TC-004: RAG Reporter Agent

| Field | Value |
|-------|-------|
| **Test ID** | TC-004 |
| **Feature** | RAG Reporter Agent |
| **Priority** | High |

**Test Data:**
```python
ALL_PROJECTS = {
    'ECOM': {'status': 'AMBER', 'health': 'At Risk'},
    'MAPP': {'status': 'GREEN', 'health': 'On Track'},
    'DPLAT': {'status': 'RED', 'health': 'Critical'},
    'SECU': {'status': 'GREEN', 'health': 'On Track'}
}
```

**Test Steps:**
1. Click "RAG Reporter Agent" or Quick Action "🚦 RAG"

**Expected Output:**
```
# 🚦 RAG Dashboard

## Portfolio Health Matrix
| PROJECT | SCHEDULE | COST | SCOPE | OVERALL |
|---------|----------|------|-------|---------|
| ECOM | 🟡 | 🟡 | 🟢 | 🟡 |
| MAPP | 🟢 | 🟢 | 🟢 | 🟢 |
| DPLAT | 🔴 | 🔴 | 🟡 | 🔴 |
| SECU | 🟢 | 🟢 | 🟢 | 🟢 |

## Summary
- 🔴 RED: 1 project (DPLAT)
- 🟡 AMBER: 1 project (ECOM)
- 🟢 GREEN: 2 projects (MAPP, SECU)
```

**Background Process:**
1. `_rag_reporter_agent()` called
2. All projects iterated
3. For each project:
   - Schedule RAG = SPI-based (≥1.0=🟢, 0.9-1.0=🟡, <0.9=🔴)
   - Cost RAG = CPI-based (same thresholds)
   - Scope RAG = % complete vs % time elapsed
   - Overall = worst of the three
4. Matrix formatted as Markdown table

**Pass Criteria:**
- [ ] All 4 projects displayed
- [ ] RAG colors match EVM data
- [ ] Summary counts accurate
- [ ] No table formatting issues

---

### TC-005: SteerCo Prep Agent

| Field | Value |
|-------|-------|
| **Test ID** | TC-005 |
| **Feature** | SteerCo Prep Agent |
| **Priority** | Medium |

**Test Steps:**
1. Click "SteerCo Prep Agent" or type "steerco"

**Expected Output:**
```
# 📋 SteerCo Prep Agent

## Executive Summary
Portfolio of 4 projects with $6.1M total budget.
Current status: 2 Green, 1 Amber, 1 Red.

## Key Decisions Required
1. DPLAT: Approve 6-week timeline extension
2. ECOM: Resource reallocation approval
3. Budget contingency release

## Risk Summary
- HIGH risks: 3
- MEDIUM risks: 2
- Mitigation plans in progress

## Financial Summary
| Metric | Value |
|--------|-------|
| Total Budget | $6.1M |
| Spent | $3.4M (56%) |
| EAC | $7.2M |
| VAC | -$1.1M |
```

**Background Process:**
1. `_steerco_prep_agent()` called
2. Portfolio-level aggregations:
   - Total budget sum
   - Total spent sum
   - Weighted CPI/SPI
3. Decision items generated from:
   - Projects with RED status
   - High-severity unresolved risks
   - Budget variances > 10%
4. Executive-friendly formatting applied

**Pass Criteria:**
- [ ] Executive summary concise (< 3 sentences)
- [ ] All sections present
- [ ] Financial data accurate
- [ ] Decisions actionable

---

### TC-006: EVM Analyst Agent

| Field | Value |
|-------|-------|
| **Test ID** | TC-006 |
| **Feature** | EVM Analyst Agent |
| **Priority** | High |

**Test Data:**
```python
DPLAT_EVM = {
    'bac': 2000000,  # Budget at Completion
    'ev': 980000,    # Earned Value
    'pv': 1200000,   # Planned Value
    'ac': 1400000    # Actual Cost
}
# Calculated:
# CPI = 980000/1400000 = 0.70
# SPI = 980000/1200000 = 0.82
```

**Test Steps:**
1. Click "EVM Analyst Agent"
2. Or type "evm DPLAT"

**Expected Output:**
```
# 📈 EVM Analyst Agent

## DPLAT - Earned Value Analysis

### Performance Indices
| Metric | Value | Status |
|--------|-------|--------|
| CPI | 0.70 | 🔴 Critical |
| SPI | 0.82 | 🔴 Critical |

### Variance Analysis
| Metric | Value |
|--------|-------|
| CV | -$420,000 |
| SV | -$220,000 |
| EAC | $2,857,143 |
| VAC | -$857,143 |

### Interpretation
- Project is 30% over budget
- Project is 18% behind schedule
- Forecast overrun: $857K
```

**Background Process:**
1. `_evm_analyst_agent("DPLAT")` called
2. `calculate_project_evm("DPLAT")` from `pmo_tools.py`
3. `evm_calculator.py` calculations:
   ```python
   CPI = EV / AC
   SPI = EV / PV
   CV = EV - AC
   SV = EV - PV
   EAC = BAC / CPI
   VAC = BAC - EAC
   TCPI = (BAC - EV) / (BAC - AC)
   ```
4. Health status determined:
   - CPI/SPI ≥ 1.0 → 🟢
   - 0.9 ≤ CPI/SPI < 1.0 → 🟡
   - CPI/SPI < 0.9 → 🔴

**Pass Criteria:**
- [ ] All EVM metrics calculated correctly
- [ ] Status indicators match thresholds
- [ ] Interpretation text accurate
- [ ] TCPI calculated for recovery guidance

---

### TC-007: ML Predictions Agent

| Field | Value |
|-------|-------|
| **Test ID** | TC-007 |
| **Feature** | ML Predictions Agent |
| **Priority** | High |

**Test Data:**
```python
# Features extracted from ECOM project
features = {
    'cpi': 0.91,
    'spi': 0.83,
    'percent_complete': 50.0,
    'risk_score': 0.0,
    'active_blockers': 2,
    'velocity': 30,
    'velocity_trend': 0,
    'team_utilization': 100,
    'bac': 1000000
}
```

**Test Steps:**
1. Navigate to "🤖 ML Predictions" tab
2. Select "ECOM" from dropdown

**Expected Output:**
```
## ML-Powered Predictions

### EVM Input Features
| Metric | Value |
|--------|-------|
| CPI | 0.91 |
| SPI | 0.83 |
| % Complete | 50.0% |
| Risk Score | 0.0 |

### Cost Forecast (XGBoost)
- Predicted Final Cost: $1,100,000
- Budget: $1,000,000
- Cost Overrun: 🟡 +10.0%
- Confidence: 82%

### Schedule Forecast (Linear Regression)
- Status: 🔴 DELAYED
- Predicted Delay: 36 days
- On-Time Probability: 82%

### Risk Classification (XGBoost)
- Risk Level: 🔴 HIGH
- Confidence: 70%
```

**Background Process:**
1. User selects project → triggers `st.selectbox` callback
2. `get_all_projects()[project]` retrieves data
3. `get_full_ml_prediction(project)` called from `ml_models.py`
4. `EVMFeatureExtractor.extract_features()` runs:
   - Extracts CPI, SPI, CV, SV from EVM data
   - Calculates risk_score from risks array
   - Computes velocity from sprints
5. Each model predicts:
   - `CostForecaster.predict()` → XGBoost regression
   - `SchedulePredictor.predict()` → Linear regression
   - `RiskClassifier.predict()` → XGBoost classification
   - `ResourceForecaster.predict()` → Linear regression
   - `BurnRatePredictor.predict()` → XGBoost regression
6. Predictions returned as dictionary
7. Plotly gauges and charts rendered

**Pass Criteria:**
- [ ] All 5 prediction models return results
- [ ] Feature extraction no errors
- [ ] Gauge charts render correctly
- [ ] Probability pie chart accurate
- [ ] Feature importance bars displayed

---

### TC-008: Handoff Demonstration

| Field | Value |
|-------|-------|
| **Test ID** | TC-008 |
| **Feature** | Agent-to-Agent Handoffs |
| **Priority** | Medium |

**Test Steps:**
1. Click "🔄 Handoff" quick action button

**Expected Output:**
```
# 📍 Handoff Demonstration Flow

### 📍 Handoff 1: Orchestrator → Risk Prediction Agent
🤖 Orchestrator: "Analyzing risks for all projects..."
[Risk Report]

### 📍 Handoff 2: Risk Prediction → EVM Analyst
🤖 Risk Prediction: "Identified budget issues..."
[EVM Report]

### 📍 Handoff 3: EVM Analyst → Escalation Agent
🤖 EVM Analyst: "Critical CPI < 0.9 detected..."
[Escalation Report]

### 📍 Handoff 4: Escalation → Resource Allocation
🤖 Escalation: "Resource constraints identified..."
[Resource Report]

### 📍 Handoff 5: Resource → Predictive Analytics
🤖 Resource: "Future bottlenecks predicted..."
[Predictive Report]
```

**Background Process:**
1. `process_query("demonstrate handoff")` called
2. `_handoff_demonstration()` method executes
3. Sequential agent calls:
   - `_risk_prediction_agent()` → detects issues
   - `_evm_analyst_agent()` → analyzes finances
   - `_escalation_agent()` → generates alerts
   - `_resource_allocation_agent()` → checks capacity
   - `_predictive_analytics_agent()` → forecasts
4. Each handoff logged with context

**Pass Criteria:**
- [ ] All 5 handoffs displayed
- [ ] Each agent's report included
- [ ] Handoff context messages clear
- [ ] No infinite loops

---

## UI Component Tests

### TC-009: Tab Navigation

| Field | Value |
|-------|-------|
| **Test ID** | TC-009 |
| **Feature** | Tab Navigation |
| **Priority** | High |

**Test Steps:**
1. Click each tab in sequence:
   - 💬 AI Assistant
   - 📊 Portfolio
   - 🔍 Deep Dive
   - ⚠️ Risks & Blockers
   - 📈 EVM Analytics
   - 📊 Visualizations
   - 🤖 ML Predictions
   - 📋 Reports

**Expected Output:**
- Each tab renders its content
- No errors
- State preserved when switching

**Pass Criteria:**
- [ ] All 8 tabs accessible
- [ ] Content loads correctly
- [ ] No layout issues
- [ ] Session state maintained

---

### TC-010: Chat Input

| Field | Value |
|-------|-------|
| **Test ID** | TC-010 |
| **Feature** | Chat Input |
| **Priority** | High |

**Test Data:**
```
Query: "portfolio overview"
```

**Test Steps:**
1. Navigate to AI Assistant tab
2. Type "portfolio overview" in chat input
3. Press Enter

**Expected Output:**
- User message displayed: "You: portfolio overview"
- CoPilot response with portfolio report
- Report appears in "Generated Report" section

**Background Process:**
1. `st.chat_input()` captures text
2. Text added to `st.session_state.messages`
3. `get_ai_response(query, use_openai)` called
4. If Demo Mode: `demo.process_query(query)`
5. Response added to messages
6. UI re-renders with `st.rerun()`

**Pass Criteria:**
- [ ] Text input visible (dark on white)
- [ ] Message sent on Enter
- [ ] Response generated
- [ ] Conversation history maintained

---

### TC-011: Quick Action Buttons

| Field | Value |
|-------|-------|
| **Test ID** | TC-011 |
| **Feature** | Quick Action Buttons |
| **Priority** | Medium |

**Test Data:**
```python
quick_actions = [
    ("📊", "Portfolio", "portfolio overview"),
    ("🚨", "Blockers", "blockers"),
    ("⚠️", "Risks", "risks"),
    ("📋", "SteerCo", "steerco"),
    ("📈", "EVM", "evm"),
    ("🚦", "RAG", "rag dashboard"),
    ("🔄", "Handoff", "demonstrate handoff")
]
```

**Test Steps:**
1. Click each quick action button
2. Verify correct query triggered

**Pass Criteria:**
- [ ] All 7 buttons visible
- [ ] Correct query for each button
- [ ] Button text readable
- [ ] Hover effect works

---

## Visualization Tests

### TC-012: Gantt Chart

| Field | Value |
|-------|-------|
| **Test ID** | TC-012 |
| **Feature** | Gantt Chart |
| **Priority** | Medium |

**Test Steps:**
1. Navigate to Visualizations tab
2. Select "📅 Gantt Chart" sub-tab

**Expected Output:**
- Timeline chart with all project milestones
- Color-coded by project
- Interactive zoom/pan

**Background Process:**
1. `get_all_projects()` fetches milestone data
2. For each project, milestones extracted
3. `px.timeline()` creates Gantt chart
4. Colors mapped: ECOM=cyan, MAPP=green, DPLAT=red, SECU=purple
5. `fig.update_layout()` applies dark theme

**Pass Criteria:**
- [ ] All milestones displayed
- [ ] Dates accurate
- [ ] Legend visible
- [ ] Zoom/pan functional

---

### TC-013: Resource Heatmap

| Field | Value |
|-------|-------|
| **Test ID** | TC-013 |
| **Feature** | Resource Heatmap |
| **Priority** | Medium |

**Test Steps:**
1. Navigate to Visualizations tab
2. Select "🌡️ Resource Heatmap" sub-tab

**Expected Output:**
- Matrix showing resource allocation %
- Color gradient: 0%=dark, 100%+=red
- Utilization summary

**Background Process:**
1. Team data extracted from all projects
2. Allocation matrix built: resources × projects
3. `px.imshow()` creates heatmap
4. Color scale: Viridis or custom gradient
5. Summary metrics calculated

**Pass Criteria:**
- [ ] All resources shown
- [ ] Percentages accurate
- [ ] Color scale correct
- [ ] Annotations visible

---

### TC-014: Burn-down Chart

| Field | Value |
|-------|-------|
| **Test ID** | TC-014 |
| **Feature** | Burn-down Chart |
| **Priority** | Medium |

**Test Data:**
```python
sprint_data = {
    'total_points': 120,
    'completed': 45,
    'days': [1, 2, 3, 4, 5, ...],
    'ideal': [120, 108, 96, ...],
    'actual': [120, 115, 105, ...]
}
```

**Test Steps:**
1. Navigate to Visualizations tab
2. Select "📉 Burn-down Chart" sub-tab
3. Select a project

**Expected Output:**
- Line chart: ideal vs actual
- Metrics: total points, completed, remaining, velocity
- Sprint selector

**Background Process:**
1. Project selected → sprint data loaded
2. Ideal line: `total_points / sprint_days`
3. Actual line: daily remaining points
4. `go.Figure()` creates chart with two traces
5. Velocity calculated: `completed / elapsed_days`

**Pass Criteria:**
- [ ] Both lines rendered
- [ ] Metrics accurate
- [ ] Sprint selection works
- [ ] Chart updates on project change

---

## Data Processing Tests

### TC-015: File Upload

| Field | Value |
|-------|-------|
| **Test ID** | TC-015 |
| **Feature** | XLSX File Upload |
| **Priority** | Medium |

**Test Data:**
- File: `Portfolio_Dashboard_Export.xlsx`
- Format: Standard JIRA export

**Test Steps:**
1. Click "Browse files" in sidebar
2. Select XLSX file
3. Wait for processing

**Expected Output:**
- Success message
- Project data updated
- Charts refresh

**Background Process:**
1. `st.file_uploader()` receives file
2. File validated: extension, size
3. `pd.read_excel()` parses data
4. Column mapping applied
5. Data merged with existing projects
6. `st.session_state` updated
7. UI refreshes

**Pass Criteria:**
- [ ] Valid XLSX accepted
- [ ] Invalid files rejected
- [ ] Data parsed correctly
- [ ] No data loss

---

### TC-016: EVM Calculator

| Field | Value |
|-------|-------|
| **Test ID** | TC-016 |
| **Feature** | EVM Calculator |
| **Priority** | High |

**Test Data:**
```python
input_values = {
    'bac': 1000000,
    'percent_complete': 50,
    'actual_cost': 600000,
    'percent_schedule': 60
}
```

**Test Steps:**
1. Navigate to EVM Analytics tab
2. Select project
3. View calculated metrics

**Expected Output:**
```
EV = 1000000 × 0.50 = 500000
PV = 1000000 × 0.60 = 600000
AC = 600000
CPI = 500000 / 600000 = 0.833
SPI = 500000 / 600000 = 0.833
CV = 500000 - 600000 = -100000
SV = 500000 - 600000 = -100000
EAC = 1000000 / 0.833 = 1200480
VAC = 1000000 - 1200480 = -200480
```

**Background Process:**
1. Project selected → `calculate_project_evm()` called
2. `evm_calculator.EVMCalculator` instantiated
3. Formulas applied
4. Results formatted with currency
5. Quadrant chart generated

**Pass Criteria:**
- [ ] Calculations mathematically correct
- [ ] Handles edge cases (div by zero)
- [ ] Formatting consistent
- [ ] Quadrant placement accurate

---

## Integration Tests

### TC-017: Demo Mode vs Live AI Mode

| Field | Value |
|-------|-------|
| **Test ID** | TC-017 |
| **Feature** | Mode Toggle |
| **Priority** | High |

**Test Steps:**
1. Ensure "Live AI Mode" is OFF
2. Submit query → verify demo response
3. Toggle "Live AI Mode" ON
4. Submit same query → verify API call attempted

**Expected Output:**
- Demo Mode: Pre-built responses, no API calls
- Live Mode: API response or error message

**Background Process:**
```python
if st.session_state.use_openai_agents:
    # Live mode
    response = await run_pmo_copilot(query)
else:
    # Demo mode
    response = demo.process_query(query)
```

**Pass Criteria:**
- [ ] Toggle works
- [ ] Demo mode reliable
- [ ] Live mode handles errors gracefully
- [ ] Mode indicator visible

---

### TC-018: Session State Persistence

| Field | Value |
|-------|-------|
| **Test ID** | TC-018 |
| **Feature** | Session State |
| **Priority** | Medium |

**Test Steps:**
1. Generate a report
2. Switch tabs
3. Return to AI Assistant
4. Verify conversation history preserved

**Expected Output:**
- Messages remain in conversation
- Last report still visible
- Selected agent maintained

**Pass Criteria:**
- [ ] Conversation history intact
- [ ] Report persists
- [ ] No state loss on tab switch

---

### TC-019: End-to-End Demo Flow

| Field | Value |
|-------|-------|
| **Test ID** | TC-019 |
| **Feature** | Complete Demo |
| **Priority** | Critical |

**Test Steps:**
1. Open app fresh
2. View Portfolio tab
3. Click DPLAT project
4. Generate escalation report
5. View EVM analysis
6. Run ML predictions
7. Generate SteerCo package

**Expected Output:**
- Each step completes successfully
- Data consistent across views
- No errors throughout flow

**Pass Criteria:**
- [ ] All steps complete
- [ ] Data consistency
- [ ] < 5 second response times
- [ ] Professional appearance

---

## Performance Tests

### TC-020: Load Time

| Field | Value |
|-------|-------|
| **Test ID** | TC-020 |
| **Feature** | Initial Load |
| **Priority** | Medium |

**Test Steps:**
1. Clear browser cache
2. Navigate to http://localhost:8501
3. Measure time to interactive

**Expected Output:**
- Page loads in < 5 seconds
- All components visible
- No layout shift

**Pass Criteria:**
- [ ] Load time < 5s
- [ ] No JavaScript errors
- [ ] All assets loaded

---

## Test Execution Checklist

### Pre-Requisites
- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Streamlit server running (`streamlit run pmo_copilot_app.py`)

### Test Environment
- Browser: Chrome/Firefox/Safari (latest)
- Resolution: 1920x1080 minimum
- Network: Local (http://localhost:8501)

### Execution Order
1. UI Component Tests (TC-009 to TC-011)
2. Agent Functionality Tests (TC-001 to TC-008)
3. Visualization Tests (TC-012 to TC-014)
4. Data Processing Tests (TC-015 to TC-016)
5. Integration Tests (TC-017 to TC-019)
6. Performance Tests (TC-020)

---

## Bug Report Template

```
**Bug ID:** BUG-XXX
**Test Case:** TC-XXX
**Severity:** Critical/High/Medium/Low
**Status:** Open/In Progress/Fixed/Closed

**Description:**
[What went wrong]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happened]

**Screenshots:**
[Attach if applicable]

**Environment:**
- OS: [macOS/Windows/Linux]
- Browser: [Chrome/Firefox/Safari]
- Version: [App version]
```

---

*Document Version: 1.0*
*Last Updated: January 2026*
*Author: PMO CoPilot QA Team*
