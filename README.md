# 🚀 PMO CoPilot

**AI-First Project Management Assistant** built with OpenAI Agents SDK

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![OpenAI Agents SDK](https://img.shields.io/badge/OpenAI_Agents-0.0.7+-412991.svg)](https://platform.openai.com/)

---

## 📋 Overview

PMO CoPilot is an intelligent multi-agent system designed for enterprise project portfolio management. It leverages the OpenAI Agents SDK for sophisticated AI-driven insights, automated reporting, and predictive analytics.

### Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **13 AI Agents** | Specialized agents for status reporting, risk prediction, escalation, EVM analysis, and more |
| 📊 **Multi-Agent Handoffs** | Agents intelligently delegate to specialists based on query context |
| 📈 **ML Predictions** | XGBoost & Linear Regression models for cost, schedule, and risk forecasting |
| 📉 **Advanced Visualizations** | Gantt charts, Resource Heatmaps, Burn-down charts |
| 🚦 **RAG Dashboard** | Real-time Red/Amber/Green portfolio health monitoring |
| 💰 **EVM Analytics** | Complete Earned Value Management with variance analysis |

---

## 🏗️ Architecture

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
└─────────┘          └─────────┘          └─────────┘
    │                      │                      │
    ▼                      ▼                      ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│   RAG   │          │ SteerCo │          │   EVM   │
│Reporter │          │  Prep   │          │ Analyst │
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

## 🤖 AI Agents

| Agent | Description | Key Outputs |
|-------|-------------|-------------|
| **Auto Orchestrator** | Routes queries to best specialist | Intelligent delegation |
| **Status Report** | Generates weekly/monthly reports | Sprint progress, metrics, blockers |
| **Risk Prediction** | Predicts delays & budget overruns | Risk assessment, mitigation plans |
| **Escalation** | Auto-escalates critical issues | Stakeholder alerts, action items |
| **RAG Reporter** | Red/Amber/Green dashboard | Portfolio health matrix |
| **SteerCo Prep** | Executive summaries | Talking points, decisions |
| **EVM Analyst** | Earned Value Management | CPI, SPI, variance analysis |
| **Schedule Optimizer** | Timeline optimization | Critical path, dependencies |
| **Resource Allocation** | Capacity analysis | Utilization matrix, reallocation |
| **Milestone Guardian** | Milestone tracking | Predictions, at-risk alerts |
| **Predictive Analytics** | ML-based forecasting | Probability analysis |
| **ML Predictions** | XGBoost/Linear Regression | Cost, schedule, risk forecasts |
| **Workflow Automation** | Bottleneck analysis | Automation opportunities |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/git-bonda108/PMO_CoPIlot.git
cd PMO_CoPIlot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# API Keys (optional - Demo mode works without them)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Model Settings
OPENAI_MODEL=gpt-4o
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Run the Application

```bash
# Using Streamlit directly
streamlit run pmo_copilot_app.py

# Or using Python module
python -m streamlit run pmo_copilot_app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
PMO_CoPIlot/
├── pmo_copilot_app.py          # Main Streamlit UI
├── pmo_copilot_agents.py       # OpenAI Agents SDK implementation
├── pmo_tools.py                # Agent tool functions
├── demo_runner.py              # Demo mode (no API keys required)
├── ml_models.py                # ML prediction models
├── evm_calculator.py           # EVM calculations
├── mock_jira_data.py           # Mock JIRA data
├── requirements.txt            # Python dependencies
├── .env                        # API keys (not in git)
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── PMO_COPILOT_FEATURES_WORKFLOW.md  # Features documentation
├── PMO_COPILOT_TEST_CASES.md   # Test cases documentation
└── *.xlsx                      # Project data exports
```

---

## 📊 Demo Mode vs Live AI Mode

| Mode | Description | API Keys Required |
|------|-------------|-------------------|
| **Demo Mode** | Pre-built responses, realistic mock data | No |
| **Live AI Mode** | Real OpenAI API calls, dynamic responses | Yes |

Toggle between modes using the sidebar switch.

---

## 🎯 Use Cases

### 1. Generate Status Report
```
Click "Status Report Agent" → Select project → View comprehensive report
```

### 2. Risk Analysis
```
Click "Risk Prediction Agent" → Get AI-predicted delays and mitigations
```

### 3. ML Predictions
```
Navigate to "ML Predictions" tab → Select project → View forecasts
```

### 4. SteerCo Package
```
Click "SteerCo Prep Agent" → Get executive summary and talking points
```

### 5. EVM Analysis
```
Navigate to "EVM Analytics" tab → View CPI, SPI, variance analysis
```

---

## 📈 ML Models

| Model | Algorithm | Target | Features |
|-------|-----------|--------|----------|
| **Cost Forecaster** | XGBoost | Final project cost | CPI, SPI, % Complete, Risk Score |
| **Schedule Predictor** | Linear Regression | Delay days | SPI, Velocity, Blockers |
| **Risk Classifier** | XGBoost | HIGH/MEDIUM/LOW | CPI, SPI, Blockers, Velocity Trend |
| **Resource Forecaster** | Linear Regression | FTEs needed | Completion %, Team Size, Velocity |
| **Burn Rate Predictor** | XGBoost | Monthly burn rate | Cost, EAC, VAC, TCPI |

---

## 📋 EVM Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| **EV** | Budget × % Complete | Earned Value |
| **PV** | Planned budget to date | Planned Value |
| **AC** | Actual spending | Actual Cost |
| **CPI** | EV / AC | Cost Performance Index |
| **SPI** | EV / PV | Schedule Performance Index |
| **CV** | EV - AC | Cost Variance |
| **SV** | EV - PV | Schedule Variance |
| **EAC** | BAC / CPI | Estimate at Completion |
| **VAC** | BAC - EAC | Variance at Completion |
| **TCPI** | (BAC-EV)/(BAC-AC) | To Complete Performance Index |

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **AI Framework:** OpenAI Agents SDK
- **ML:** scikit-learn, XGBoost
- **Visualization:** Plotly
- **Data Processing:** Pandas, NumPy

---

## 📄 Documentation

- [Features & Workflow Guide](PMO_COPILOT_FEATURES_WORKFLOW.md)
- [Test Cases](PMO_COPILOT_TEST_CASES.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is proprietary software developed for IgniteTech.

---

## 👤 Author

**PMO CoPilot Development Team**

- Built for IgniteTech Interview Demo
- January 2026

---

## 🙏 Acknowledgments

- OpenAI for the Agents SDK
- Streamlit for the web framework
- Plotly for visualizations
