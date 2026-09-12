# PMO CoPilot - Features & Workflow Documentation

## 📋 Overview

**PMO CoPilot** is an AI-First Project Management Assistant for enterprise PMO teams, leveraging the OpenAI Agents SDK for intelligent multi-agent orchestration. It provides real-time project insights, predictive analytics, and automated reporting capabilities.

---

## 🏗️ Architecture

### Technology Stack
- **Frontend:** Streamlit (Python web framework)
- **AI Framework:** OpenAI Agents SDK
- **ML Models:** scikit-learn, XGBoost (fallback: GradientBoosting)
- **Data Visualization:** Plotly
- **Data Processing:** Pandas, NumPy

### Multi-Agent Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR AGENT                          │
│         (Routes queries to appropriate specialist agents)        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│ Status  │          │  Risk   │          │Escalation│
│ Report  │          │Prediction│         │  Agent   │
│ Agent   │          │  Agent  │          │          │
└─────────┘          └─────────┘          └─────────┘
    │                      │                      │
    ▼                      ▼                      ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│   RAG   │          │ SteerCo │          │   EVM   │
│Reporter │          │  Prep   │          │ Analyst │
│  Agent  │          │  Agent  │          │  Agent  │
└─────────┘          └─────────┘          └─────────┘
    │                      │                      │
    ▼                      ▼                      ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│Schedule │          │Resource │          │Milestone│
│Optimizer│          │Allocation│         │Guardian │
└─────────┘          └─────────┘          └─────────┘
    │                      │                      │
    ▼                      ▼                      ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│Predictive│         │Workflow │          │   ML    │
│Analytics │         │Automation│         │Predictions│
└─────────┘          └─────────┘          └─────────┘
```

---

## 🤖 AI Agents & Features

### 1. Auto Orchestrator
**Purpose:** Intelligently routes user queries to the most appropriate specialist agent.

**How it works:**
1. User submits a natural language query
2. Orchestrator analyzes intent using keyword matching and context
3. Routes to appropriate specialist agent
4. Returns consolidated response

**Handoff Capability:** Can delegate to any specialist agent based on detected issues.

---

### 2. Status Report Agent
**Purpose:** Generates comprehensive weekly/monthly status reports.

**Output includes:**
- Project health overview (🟢 Green, 🟡 Amber, 🔴 Red)
- Sprint progress and velocity
- Issue breakdown (Stories, Bugs, Tasks)
- Key accomplishments and blockers
- Recommendations

**Data sources:** JIRA exports, project metadata

---

### 3. Risk Prediction Agent
**Purpose:** Analyzes project data to predict delays, budget overruns, and scope creep.

**Analysis includes:**
- Active risks with severity ratings
- Probability and impact assessment
- Risk trends over time
- Mitigation recommendations

**Handoffs to:** Escalation Agent (critical risks), EVM Analyst (budget risks)

---

### 4. Escalation Agent
**Purpose:** Identifies blockers and auto-escalates to stakeholders.

**Features:**
- Blocker identification and age tracking
- Escalation priority matrix
- Stakeholder notification templates
- Critical path impact analysis

**Triggers:**
- Blockers > 5 days old
- CPI < 0.9 or SPI < 0.9
- High severity risks unresolved

---

### 5. RAG Reporter Agent
**Purpose:** Real-time Red/Amber/Green dashboard with AI insights.

**Dashboard includes:**
- Portfolio health matrix
- RAG breakdown by project
- Trend analysis
- AI-generated insights and recommendations

**Color coding:**
- 🔴 RED: Critical issues, immediate action required
- 🟡 AMBER: At risk, monitoring required
- 🟢 GREEN: On track

---

### 6. SteerCo Prep Agent
**Purpose:** Auto-generates executive summaries and talking points.

**Package includes:**
- Executive summary
- Portfolio overview
- Key decisions required
- Risk summary
- Financial summary (EVM)
- Recommended actions

---

### 7. EVM Analyst Agent
**Purpose:** Earned Value Management with variance analysis.

**Metrics calculated:**
| Metric | Formula | Description |
|--------|---------|-------------|
| EV | Budget × % Complete | Earned Value |
| PV | Planned budget to date | Planned Value |
| AC | Actual spending | Actual Cost |
| CPI | EV / AC | Cost Performance Index |
| SPI | EV / PV | Schedule Performance Index |
| CV | EV - AC | Cost Variance |
| SV | EV - PV | Schedule Variance |
| EAC | BAC / CPI | Estimate at Completion |
| VAC | BAC - EAC | Variance at Completion |
| TCPI | (BAC-EV)/(BAC-AC) | To Complete Performance Index |

**Health indicators:**
- CPI/SPI ≥ 1.0: Good performance
- 0.9 ≤ CPI/SPI < 1.0: Watch
- CPI/SPI < 0.9: Critical

---

### 8. Schedule Optimizer Agent
**Purpose:** Optimizes timeline, dependencies, and critical path.

**Analysis includes:**
- Current schedule status
- Milestone tracking
- Critical path identification
- Resource constraint impacts
- Optimization recommendations

---

### 9. Resource Allocation Agent
**Purpose:** Analyzes team capacity and workload distribution.

**Output:**
- Team utilization matrix
- Over/under-allocated resources
- Skill gap analysis
- Reallocation recommendations

---

### 10. Milestone Guardian Agent
**Purpose:** Tracks milestones and predicts delivery dates.

**Features:**
- Milestone status tracking
- Completion predictions
- At-risk milestone alerts
- Historical trend analysis

---

### 11. Predictive Analytics Agent
**Purpose:** ML-based forecasting and probability analysis.

**Predictions:**
- Delay probability
- Budget burn rate forecast
- Completion date estimates
- Risk escalation likelihood

---

### 12. ML Predictions Agent
**Purpose:** XGBoost & Linear Regression cost/schedule forecasts.

**Models:**
1. **Cost Forecaster (XGBoost)** - Predicts final project cost
2. **Schedule Predictor (Linear Regression)** - Predicts delay days
3. **Risk Classifier (XGBoost)** - Classifies HIGH/MEDIUM/LOW risk
4. **Resource Forecaster (Linear Regression)** - Predicts required FTEs
5. **Burn Rate Predictor (XGBoost)** - Forecasts monthly burn rate

**Input Features (EVM Metrics):**
- CPI (Cost Performance Index)
- SPI (Schedule Performance Index)
- % Complete
- Risk Score
- Active Blockers
- Velocity Trend
- Team Utilization

---

### 13. Workflow Automation Agent
**Purpose:** Analyzes bottlenecks and automation opportunities.

**Analysis:**
- Process bottlenecks
- WIP limits violations
- Automation suggestions
- Efficiency metrics

---

## 📊 UI Components

### Main Tabs
1. **💬 AI Assistant** - Chat interface with quick actions
2. **📊 Portfolio** - Portfolio overview with health metrics
3. **🔍 Deep Dive** - Detailed project analysis
4. **⚠️ Risks & Blockers** - Risk and blocker management
5. **📈 EVM Analytics** - Earned Value Management dashboard
6. **📊 Visualizations** - Gantt, Heatmap, Burn-down charts
7. **🤖 ML Predictions** - Machine learning predictions dashboard
8. **📋 Reports** - Report generator

### Sidebar
- Live AI Mode toggle
- Agent selection buttons (13 agents)
- Project portfolio summary
- Data import (XLSX upload)

---

## 🔄 End-to-End Workflow

### Workflow 1: Generate Status Report
```
User clicks "Status Report Agent" button
         ↓
System identifies selected agent
         ↓
Query sent to demo_runner.process_query()
         ↓
_status_report_agent() method called
         ↓
get_portfolio_overview() fetches project data
         ↓
Report formatted with Markdown
         ↓
Report displayed in "Generated Report" section
```

### Workflow 2: ML Prediction Analysis
```
User navigates to "ML Predictions" tab
         ↓
ml_models.py loaded (imports sklearn/xgboost)
         ↓
User selects project from dropdown
         ↓
EVMFeatureExtractor.extract_features() runs
         ↓
Features sent to 5 ML models
         ↓
get_full_ml_prediction() returns:
  - cost_forecast
  - schedule_forecast
  - risk_classification
  - resource_forecast
  - burn_rate_forecast
         ↓
Plotly gauges and charts rendered
         ↓
Feature importance displayed
```

### Workflow 3: Agent-to-Agent Handoff
```
User asks: "comprehensive analysis DPLAT"
         ↓
Orchestrator identifies complex query
         ↓
Routes to Risk Prediction Agent
         ↓
Risk Agent detects EVM issues
         ↓
Handoff → EVM Analyst Agent
         ↓
EVM Agent finds CPI < 0.9
         ↓
Handoff → Escalation Agent
         ↓
Escalation Agent generates urgent report
         ↓
Handoff → Resource Allocation Agent
         ↓
Resource Agent analyzes capacity
         ↓
Consolidated response returned
```

### Workflow 4: Chat Query Processing
```
User types query in chat input
         ↓
st.chat_input captures text
         ↓
Check if Live AI Mode enabled:
  YES → pmo_copilot_agents.run_pmo_copilot()
  NO → demo_runner.process_query()
         ↓
Response added to conversation history
         ↓
Report rendered with st.markdown()
```

### Workflow 5: Data Upload
```
User uploads XLSX file via file_uploader
         ↓
File validated (format, size)
         ↓
pandas.read_excel() processes data
         ↓
Data mapped to project structure
         ↓
session_state updated with new data
         ↓
UI refreshes with new project data
```

---

## 📁 File Structure

```
PMO_CoPIlot/
├── pmo_copilot_app.py      # Main Streamlit UI
├── pmo_copilot_agents.py   # OpenAI Agents SDK implementation
├── pmo_tools.py            # Agent tool functions
├── demo_runner.py          # Demo mode (no API keys)
├── ml_models.py            # ML prediction models
├── evm_calculator.py       # EVM calculations
├── mock_jira_data.py       # Mock JIRA data
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not in git)
└── Excel files             # Project data exports
```

---

## 🔐 Security & Configuration

### Environment Variables
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_MODEL=gpt-4o
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Demo Mode
When Live AI Mode is OFF, the system uses demo_runner.py which provides:
- Pre-built responses for all agent types
- Realistic mock data
- No API calls required
- Suitable for demos and testing

---

## 📈 Performance Metrics

### Response Times (Demo Mode)
- Status Report: ~100ms
- EVM Analysis: ~150ms
- ML Predictions: ~500ms (model training)
- Chart Rendering: ~200ms

### ML Model Accuracy (Simulated)
- Cost Forecaster: 85% confidence
- Schedule Predictor: 75-90% confidence
- Risk Classifier: 70-82% confidence

---

## 🚀 Future Enhancements

1. **Real JIRA Integration** - OAuth authentication, real-time sync
2. **PDF Export** - Downloadable reports
3. **Email Notifications** - Automated alerts
4. **Historical Trends** - Time-series analysis
5. **Custom Dashboards** - User-configurable views

---

*Document Version: 1.0*
*Last Updated: January 2026*
