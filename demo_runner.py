"""
PMO CoPilot - Demo Runner
This file demonstrates the system without requiring OpenAI API keys.
It simulates agent responses using the actual tool functions.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

# Import our tools
from pmo_tools import (
    get_portfolio_overview,
    get_project_details,
    get_project_blockers,
    get_project_risks,
    calculate_project_evm,
    get_sprint_status,
    get_issue_breakdown,
    generate_escalation_report,
    get_schedule_analysis,
    get_resource_allocation,
    get_milestone_status,
    get_predictive_analytics,
    get_workflow_status,
)
from mock_jira_data import get_all_projects, get_project_summary

class PMOCoPilotDemo:
    """
    Demo version of PMO CoPilot that works without API keys.
    Simulates the multi-agent behavior using direct tool calls.
    """

    def __init__(self):
        self.agents = {
            "status": self._status_report_agent,
            "risk": self._risk_prediction_agent,
            "escalation": self._escalation_agent,
            "rag": self._rag_reporter_agent,
            "steerco": self._steerco_prep_agent,
            "evm": self._evm_analyst_agent,
            "schedule": self._schedule_optimizer_agent,
            "resource": self._resource_allocation_agent,
            "milestone": self._milestone_guardian_agent,
            "predictive": self._predictive_analytics_agent,
            "workflow": self._workflow_automation_agent,
        }

    def process_query(self, query: str) -> str:
        """Process a user query and return appropriate response."""
        query_lower = query.lower()

        # HANDOFF DEMONSTRATION - comprehensive analysis triggers multi-agent chains
        if any(word in query_lower for word in ["comprehensive", "full analysis", "deep dive", "complete review", "multi-agent", "handoff"]):
            project = self._extract_project(query)
            return self._comprehensive_handoff_analysis(project)

        # Route to appropriate agent based on keywords (more specific first)
        
        # NEW AGENTS - check first as they have specific keywords
        if any(word in query_lower for word in ["schedule", "timeline", "optim", "critical path", "dependency"]):
            project = self._extract_project(query)
            return self._schedule_optimizer_agent(project)

        elif any(word in query_lower for word in ["resource", "allocation", "capacity", "utilization"]):
            project = self._extract_project(query)
            return self._resource_allocation_agent(project)

        elif any(word in query_lower for word in ["milestone", "guardian", "deadline", "due date"]):
            project = self._extract_project(query)
            return self._milestone_guardian_agent(project)

        elif any(word in query_lower for word in ["ml", "machine learning", "xgboost", "regression"]):
            project = self._extract_project(query)
            return self._ml_predictions_agent(project)
        
        elif any(word in query_lower for word in ["predictive", "probability", "forecast", "analytics"]):
            project = self._extract_project(query)
            return self._predictive_analytics_agent(project)

        elif any(word in query_lower for word in ["workflow", "automation", "bottleneck", "wip", "efficiency"]):
            return self._workflow_automation_agent()

        # EXISTING AGENTS
        elif any(word in query_lower for word in ["portfolio", "overview", "all projects"]):
            return self._portfolio_overview()

        elif any(word in query_lower for word in ["status", "report", "weekly", "monthly"]):
            project = self._extract_project(query)
            return self._status_report_agent(project)

        elif any(word in query_lower for word in ["risk", "predict"]):
            project = self._extract_project(query)
            return self._risk_prediction_agent(project)

        elif any(word in query_lower for word in ["escalat", "critical", "urgent"]):
            project = self._extract_project(query)
            return self._escalation_agent(project)

        elif any(word in query_lower for word in ["rag", "dashboard", "health"]):
            return self._rag_reporter_agent()

        elif any(word in query_lower for word in ["steerco", "steering", "executive", "board"]):
            return self._steerco_prep_agent()

        elif any(word in query_lower for word in ["evm", "earned value", "cpi", "spi", "variance"]):
            project = self._extract_project(query)
            return self._evm_analyst_agent(project)

        elif any(word in query_lower for word in ["blocker", "blocked", "impediment"]):
            project = self._extract_project(query)
            return get_project_blockers(project)

        elif any(word in query_lower for word in ["sprint", "velocity", "agile"]):
            project = self._extract_project(query)
            if project:
                return get_sprint_status(project)
            return "Please specify a project (ECOM, MAPP, DPLAT, or SECU)"

        elif any(word in query_lower for word in ["issue", "ticket", "story", "bug"]):
            project = self._extract_project(query)
            if project:
                return get_issue_breakdown(project)
            return "Please specify a project (ECOM, MAPP, DPLAT, or SECU)"

        elif any(word in query_lower for word in ["detail", "about", "tell me"]):
            project = self._extract_project(query)
            if project:
                return get_project_details(project)
            return self._portfolio_overview()

        else:
            return self._default_response(query)

    def _extract_project(self, query: str) -> str:
        """Extract project key from query."""
        query_upper = query.upper()
        for key in ["ECOM", "MAPP", "DPLAT", "SECU"]:
            if key in query_upper:
                return key

        # Check for project name mentions
        query_lower = query.lower()
        if "commerce" in query_lower or "ecommerce" in query_lower:
            return "ECOM"
        elif "mobile" in query_lower or "app" in query_lower:
            return "MAPP"
        elif "data" in query_lower or "platform" in query_lower:
            return "DPLAT"
        elif "security" in query_lower or "soc2" in query_lower or "compliance" in query_lower:
            return "SECU"

        return None

    def _comprehensive_handoff_analysis(self, project: str = None) -> str:
        """
        Demonstrate multi-agent handoff capabilities.
        Shows how agents automatically delegate to specialists.
        """
        output = "# 🔄 Multi-Agent Handoff Analysis\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        output += "---\n\n"
        
        # Step 1: Risk Agent detects issues and hands off
        output += "## 🔗 Agent Handoff Chain Demonstration\n\n"
        output += "This analysis demonstrates intelligent agent-to-agent delegation.\n\n"
        
        # HANDOFF 1: Risk → EVM (Budget concerns)
        output += "### 📍 Handoff 1: Risk Agent → EVM Analyst\n"
        output += "*Risk Agent detected budget concerns, delegating to EVM specialist...*\n\n"
        output += "```\n"
        output += "🤖 Risk Agent: \"I've identified cost risk on DPLAT (CPI: 0.78).\n"
        output += "   → Handing off to EVM Analyst for financial recovery analysis.\"\n"
        output += "```\n\n"
        
        # Show EVM analysis
        output += "**EVM Analyst Response:**\n"
        evm_data = calculate_project_evm("DPLAT")
        output += f"{evm_data}\n\n"
        
        # HANDOFF 2: EVM → Escalation (Critical variance)
        output += "---\n\n"
        output += "### 📍 Handoff 2: EVM Analyst → Escalation Agent\n"
        output += "*EVM Analyst found TCPI > 1.2, delegating to Escalation for executive alert...*\n\n"
        output += "```\n"
        output += "🤖 EVM Analyst: \"TCPI of 1.28 indicates recovery is very difficult.\n"
        output += "   → Handing off to Escalation Agent for executive decision.\"\n"
        output += "```\n\n"
        
        # Show escalation
        output += "**Escalation Agent Response:**\n"
        escalation_data = generate_escalation_report("DPLAT")
        output += f"{escalation_data}\n\n"
        
        # HANDOFF 3: Schedule → Resource (Resource constraint)
        output += "---\n\n"
        output += "### 📍 Handoff 3: Schedule Optimizer → Resource Allocation\n"
        output += "*Schedule Agent detected resource constraint affecting timeline...*\n\n"
        output += "```\n"
        output += "🤖 Schedule Optimizer: \"Schedule delays linked to resource availability.\n"
        output += "   → Handing off to Resource Allocation Agent for capacity analysis.\"\n"
        output += "```\n\n"
        
        # Show resource analysis
        output += "**Resource Allocation Agent Response:**\n"
        resource_data = get_resource_allocation()
        output += f"{resource_data}\n\n"
        
        # HANDOFF 4: Milestone → Predictive (Delivery probability)
        output += "---\n\n"
        output += "### 📍 Handoff 4: Milestone Guardian → Predictive Analytics\n"
        output += "*Milestone Agent found at-risk deadlines, requesting probability forecast...*\n\n"
        output += "```\n"
        output += "🤖 Milestone Guardian: \"Q1 milestone at risk for ECOM project.\n"
        output += "   → Handing off to Predictive Analytics for delivery probability.\"\n"
        output += "```\n\n"
        
        # Show predictive analysis
        output += "**Predictive Analytics Agent Response:**\n"
        predictive_data = get_predictive_analytics("ECOM")
        output += f"{predictive_data}\n\n"
        
        # Summary
        output += "---\n\n"
        output += "## 🎯 Consolidated Multi-Agent Insights\n\n"
        output += "The handoff chain revealed:\n\n"
        output += "| Agent | Finding | Handoff Reason |\n"
        output += "|-------|---------|----------------|\n"
        output += "| Risk Agent | Budget risk (CPI 0.78) | Needed EVM deep-dive |\n"
        output += "| EVM Analyst | TCPI > 1.2 unrecoverable | Required executive escalation |\n"
        output += "| Schedule Optimizer | Resource bottleneck | Needed capacity analysis |\n"
        output += "| Milestone Guardian | Q1 deadline at risk | Needed probability forecast |\n\n"
        
        output += "### 🚨 Recommended Actions\n"
        output += "1. **IMMEDIATE**: Schedule executive meeting for DPLAT budget decision\n"
        output += "2. **THIS WEEK**: Reallocate 2 engineers from MAPP to DPLAT\n"
        output += "3. **URGENT**: De-scope ECOM Phase 2 to protect Q1 milestone\n"
        output += "4. **MONITOR**: Track SECU closely - currently on track but tight timeline\n\n"
        
        output += "*This analysis demonstrates how PMO CoPilot's multi-agent architecture*\n"
        output += "*automatically chains specialists for comprehensive insights.*\n"
        
        return output

    def _portfolio_overview(self) -> str:
        """Generate portfolio overview."""
        output = "# 🎯 PMO CoPilot - Portfolio Overview\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        output += get_portfolio_overview()

        # Add AI insight
        output += "\n### 🤖 AI Insight\n"
        output += "Based on current portfolio health, I recommend focusing attention on:\n"
        output += "1. **DPLAT (Data Platform)** - RED status with 3 critical blockers\n"
        output += "2. **ECOM (E-Commerce)** - AMBER status with payment integration delays\n\n"
        output += "The Mobile App and Security projects are performing well.\n"

        return output

    def _status_report_agent(self, project: str = None) -> str:
        """Generate status report."""
        output = "# 📊 Status Report Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        if project:
            output += get_project_details(project)
            output += "\n---\n"
            output += get_sprint_status(project)
            output += "\n---\n"
            output += get_issue_breakdown(project)
        else:
            output += get_portfolio_overview()
            output += "\n---\n"
            output += "### Key Highlights This Week\n"
            output += "- ✅ Mobile App Alpha release completed on schedule\n"
            output += "- ✅ SOC2 policies approved by compliance\n"
            output += "- ⚠️ E-Commerce checkout blocked by critical bug\n"
            output += "- 🔴 Data Platform facing data corruption issues\n"

        return output

    def _risk_prediction_agent(self, project: str = None) -> str:
        """Generate risk analysis."""
        output = "# ⚠️ Risk Prediction Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        output += get_project_risks(project)
        output += "\n---\n"
        output += get_project_blockers(project)

        # Add predictive analysis
        output += "\n### 🔮 Predictive Analysis\n\n"

        if project == "DPLAT" or project is None:
            output += "**Data Platform (DPLAT) - HIGH RISK**\n"
            output += "- 📉 Velocity declining: 35 → 32 → 28 → 25 → 18\n"
            output += "- 🔴 Based on current CPI (0.857), project will exceed budget by ~$675,000\n"
            output += "- ⏰ Based on current SPI (0.800), project will be delayed by ~6-8 weeks\n"
            output += "- 📊 Probability of on-time delivery: **15%**\n\n"

        if project == "ECOM" or project is None:
            output += "**E-Commerce (ECOM) - MEDIUM RISK**\n"
            output += "- 📉 Velocity declining: 42 → 38 → 35 → 28\n"
            output += "- 🟡 Payment integration blocker may cause 2-week delay\n"
            output += "- 📊 Probability of on-time delivery: **65%**\n\n"

        output += "### 💡 Recommendations\n"
        output += "1. Escalate DPLAT data corruption issue to CTO immediately\n"
        output += "2. Fast-track Stripe API credentials for ECOM\n"
        output += "3. Consider scope reduction for DPLAT ML integration\n"

        return output

    def _escalation_agent(self, project: str = None) -> str:
        """Generate escalation report."""
        output = "# 🚨 Escalation Agent\n\n"

        if project:
            output += generate_escalation_report(project)
        else:
            # Find projects needing escalation
            output += "## Projects Requiring Escalation\n\n"

            output += "### 🔴 CRITICAL: Data Platform Modernization (DPLAT)\n"
            output += generate_escalation_report("DPLAT")

            output += "\n---\n"
            output += "### 🟡 HIGH: E-Commerce Platform Migration (ECOM)\n"
            output += generate_escalation_report("ECOM")

        return output

    def _rag_reporter_agent(self, project: str = None) -> str:
        """Generate RAG dashboard."""
        output = "# 🚦 RAG Dashboard\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        output += "## Portfolio Health Matrix\n\n"
        output += "| PROJECT | SCHEDULE | COST | SCOPE | OVERALL |\n"
        output += "|---------|----------|------|-------|--------|\n"
        output += "| ECOM (E-Commerce) | 🟡 | 🟡 | 🟢 | 🟡 |\n"
        output += "| MAPP (Mobile App) | 🟢 | 🟢 | 🟢 | 🟢 |\n"
        output += "| DPLAT (Data) | 🔴 | 🔴 | 🟡 | 🔴 |\n"
        output += "| SECU (Security) | 🟢 | 🟢 | 🟢 | 🟢 |\n\n"

        output += "## RAG Breakdown\n\n"
        output += "### 🔴 RED Projects (1)\n"
        output += "**DPLAT - Data Platform Modernization**\n"
        output += "- CPI: 0.857 (below 0.9 threshold)\n"
        output += "- SPI: 0.800 (below 0.9 threshold)\n"
        output += "- 3 critical blockers active\n"
        output += "- Trend: 📉 Declining\n\n"

        output += "### 🟡 AMBER Projects (1)\n"
        output += "**ECOM - E-Commerce Platform Migration**\n"
        output += "- CPI: 0.800 (below 0.9 threshold)\n"
        output += "- SPI: 0.800 (below 0.9 threshold)\n"
        output += "- 2 blockers (1 critical)\n"
        output += "- Trend: ➡️ Stable\n\n"

        output += "### 🟢 GREEN Projects (2)\n"
        output += "**MAPP - Customer Mobile App v2.0**\n"
        output += "- CPI: 1.050 (above target)\n"
        output += "- SPI: 1.050 (above target)\n"
        output += "- No blockers\n"
        output += "- Trend: 📈 Improving\n\n"

        output += "**SECU - SOC2 Compliance Initiative**\n"
        output += "- CPI: 1.050 (above target)\n"
        output += "- SPI: 1.050 (above target)\n"
        output += "- No blockers\n"
        output += "- Trend: 📈 Improving\n"

        return output

    def _steerco_prep_agent(self) -> str:
        """Generate SteerCo materials."""
        output = "# 📋 SteerCo Preparation Package\n\n"
        output += f"*Prepared for: Steering Committee Meeting*\n"
        output += f"*Date: {datetime.now().strftime('%Y-%m-%d')}*\n\n"

        output += "---\n"
        output += "## 1. Executive Dashboard\n\n"
        output += self._rag_reporter_agent()

        output += "\n---\n"
        output += "## 2. Financial Summary\n\n"
        output += "| Project | Budget | Spent | EAC | Variance |\n"
        output += "|---------|--------|-------|-----|----------|\n"
        output += "| ECOM | $2.5M | $1.875M | $3.125M | -$625K 🔴 |\n"
        output += "| MAPP | $1.8M | $0.9M | $1.714M | +$86K 🟢 |\n"
        output += "| DPLAT | $4.5M | $3.15M | $5.25M | -$750K 🔴 |\n"
        output += "| SECU | $0.8M | $0.32M | $0.762M | +$38K 🟢 |\n"
        output += "| **TOTAL** | **$9.6M** | **$6.245M** | **$10.85M** | **-$1.25M** |\n\n"

        output += "---\n"
        output += "## 3. Decisions Required\n\n"
        output += "### Decision 1: DPLAT Budget Increase\n"
        output += "- **Issue:** Project projected to exceed budget by $750K\n"
        output += "- **Options:**\n"
        output += "  - A) Approve additional $750K funding\n"
        output += "  - B) Reduce scope (remove ML integration)\n"
        output += "  - C) Extend timeline by 3 months\n"
        output += "- **Recommendation:** Option B - Defer ML to Phase 2\n"
        output += "- **Decision Deadline:** Jan 31, 2026\n\n"

        output += "### Decision 2: ECOM Payment Provider\n"
        output += "- **Issue:** Stripe integration blocked by credential delays\n"
        output += "- **Options:**\n"
        output += "  - A) Continue waiting for Stripe (risk: 2-week delay)\n"
        output += "  - B) Switch to PayPal (risk: rework cost ~$50K)\n"
        output += "- **Recommendation:** Option A with escalation to Finance\n"
        output += "- **Decision Deadline:** Jan 25, 2026\n\n"

        output += "---\n"
        output += "## 4. Talking Points\n\n"
        output += "### Key Messages\n"
        output += "1. Portfolio is 65% on track (2 of 4 projects GREEN)\n"
        output += "2. DPLAT requires immediate attention and decision\n"
        output += "3. Mobile App exceeding expectations - potential early delivery\n"
        output += "4. SOC2 audit on track for May completion\n\n"

        output += "### Anticipated Questions\n"
        output += "- **Q: Why is DPLAT so far behind?**\n"
        output += "  - A: Data corruption issue discovered in ETL, ML team reassigned\n"
        output += "- **Q: Can we recover ECOM timeline?**\n"
        output += "  - A: Yes, if Stripe credentials received by Jan 25\n"
        output += "- **Q: What's the total budget impact?**\n"
        output += "  - A: Currently projecting $1.25M overrun across portfolio\n"

        return output

    def _evm_analyst_agent(self, project: str = None) -> str:
        """Generate EVM analysis."""
        output = "# 📈 EVM Analysis Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        if project:
            output += calculate_project_evm(project)
        else:
            output += "## Portfolio EVM Summary\n\n"
            for key in ["ECOM", "MAPP", "DPLAT", "SECU"]:
                output += f"### {key}\n"
                output += calculate_project_evm(key)
                output += "\n---\n"

        return output

    def _schedule_optimizer_agent(self, project: str = None) -> str:
        """Generate schedule optimization analysis."""
        output = "# 📅 Schedule Optimizer Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        output += get_schedule_analysis(project)
        
        output += "\n### 💡 AI Optimization Recommendations\n\n"
        output += "1. **Critical Path Focus:** Prioritize tasks on the critical path to prevent delays\n"
        output += "2. **Resource Leveling:** Consider reassigning resources from green projects to red\n"
        output += "3. **Buffer Management:** Add schedule buffers for at-risk milestones\n"
        output += "4. **Parallel Execution:** Identify tasks that can run in parallel to compress timeline\n"
        
        return output

    def _resource_allocation_agent(self, project: str = None) -> str:
        """Generate resource allocation analysis."""
        output = "# 👥 Resource Allocation Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        output += get_resource_allocation(project)
        
        output += "\n### 💡 AI Allocation Recommendations\n\n"
        output += "1. **Balance Workload:** Redistribute tasks from over-allocated to under-utilized resources\n"
        output += "2. **Skill Matching:** Ensure resource skills align with assigned tasks\n"
        output += "3. **Contingency Planning:** Identify backup resources for critical roles\n"
        output += "4. **Training Gaps:** Address skill gaps through training or hiring\n"
        
        return output

    def _milestone_guardian_agent(self, project: str = None) -> str:
        """Generate milestone tracking report."""
        output = "# 🎯 Milestone Guardian Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        output += get_milestone_status(project)
        
        output += "\n### 💡 AI Guardian Recommendations\n\n"
        output += "1. **Early Warning System:** Monitor leading indicators 2 weeks before milestones\n"
        output += "2. **Dependency Tracking:** Ensure predecessor tasks complete on time\n"
        output += "3. **Escalation Protocol:** Escalate at-risk milestones immediately\n"
        output += "4. **Recovery Planning:** Develop contingency plans for delayed milestones\n"
        
        return output

    def _predictive_analytics_agent(self, project: str = None) -> str:
        """Generate predictive analytics report."""
        output = "# 🔮 Predictive Analytics Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        output += get_predictive_analytics(project)
        
        output += "\n### 💡 AI Predictions Summary\n\n"
        output += "Based on current trends and historical data:\n\n"
        output += "| Project | On-Time Probability | Cost Risk | Action |\n"
        output += "|---------|---------------------|-----------|--------|\n"
        output += "| DPLAT | 15% | 🔴 HIGH | Immediate intervention |\n"
        output += "| ECOM | 65% | 🟡 MEDIUM | Close monitoring |\n"
        output += "| MAPP | 90% | 🟢 LOW | Continue current pace |\n"
        output += "| SECU | 85% | 🟢 LOW | On track |\n"
        
        return output

    def _ml_predictions_agent(self, project: str = None) -> str:
        """Generate ML-powered predictions using Linear Regression and XGBoost."""
        output = "# 🤖 ML-Powered Predictive Analytics\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
        output += "*Models: Linear Regression, XGBoost*\n\n"
        
        # Try to use actual ML models
        try:
            from pmo_tools import get_ml_predictions
            ml_output = get_ml_predictions(project)
            output += ml_output
        except Exception as e:
            # Fallback to demo data
            output += self._generate_ml_demo_data(project)
        
        return output
    
    def _generate_ml_demo_data(self, project: str = None) -> str:
        """Generate demo ML prediction data."""
        projects_data = {
            'DPLAT': {
                'cpi': 0.85, 'spi': 0.78,
                'cost_overrun': 18.5, 'delay_days': 45,
                'risk_level': 'HIGH', 'risk_prob': 0.82,
                'required_ftes': 12.5, 'current_ftes': 8,
                'burn_variance': 15.2
            },
            'ECOM': {
                'cpi': 0.92, 'spi': 0.88,
                'cost_overrun': 8.7, 'delay_days': 18,
                'risk_level': 'MEDIUM', 'risk_prob': 0.65,
                'required_ftes': 10.2, 'current_ftes': 9,
                'burn_variance': 8.5
            },
            'MAPP': {
                'cpi': 1.05, 'spi': 1.02,
                'cost_overrun': -4.8, 'delay_days': -5,
                'risk_level': 'LOW', 'risk_prob': 0.15,
                'required_ftes': 7.8, 'current_ftes': 8,
                'burn_variance': -3.2
            },
            'SECU': {
                'cpi': 1.02, 'spi': 0.98,
                'cost_overrun': -1.9, 'delay_days': 3,
                'risk_level': 'LOW', 'risk_prob': 0.22,
                'required_ftes': 5.5, 'current_ftes': 6,
                'burn_variance': 2.1
            }
        }
        
        if project and project.upper() in projects_data:
            projects_to_show = {project.upper(): projects_data[project.upper()]}
        else:
            projects_to_show = projects_data
        
        output = ""
        
        for key, data in projects_to_show.items():
            output += f"### 📊 {key}\n\n"
            
            # Input Features
            output += "#### 📈 Input Features (EVM Metrics)\n"
            output += f"| Metric | Value |\n|--------|-------|\n"
            output += f"| CPI | {data['cpi']:.2f} |\n"
            output += f"| SPI | {data['spi']:.2f} |\n\n"
            
            # Cost Forecast
            cost_emoji = "🔴" if data['cost_overrun'] > 10 else ("🟡" if data['cost_overrun'] > 0 else "🟢")
            output += "#### 💰 Cost Forecast (XGBoost)\n"
            output += f"- **Cost Overrun:** {cost_emoji} {data['cost_overrun']:+.1f}%\n"
            output += f"- **Confidence:** 85%\n\n"
            
            # Schedule Forecast
            sched_emoji = "🔴" if data['delay_days'] > 20 else ("🟡" if data['delay_days'] > 5 else "🟢")
            output += "#### 📅 Schedule Forecast (Linear Regression)\n"
            output += f"- **Predicted Delay:** {sched_emoji} {data['delay_days']:+.0f} days\n"
            output += f"- **On-Time Probability:** {max(0, 100 - data['delay_days'] * 2):.0f}%\n\n"
            
            # Risk Classification
            risk_emoji = "🔴" if data['risk_level'] == 'HIGH' else ("🟡" if data['risk_level'] == 'MEDIUM' else "🟢")
            output += "#### ⚠️ Risk Classification (XGBoost)\n"
            output += f"- **Risk Level:** {risk_emoji} {data['risk_level']}\n"
            output += f"- **Confidence:** {data['risk_prob']*100:.0f}%\n\n"
            
            # Resource Forecast
            delta = data['required_ftes'] - data['current_ftes']
            delta_emoji = "➕" if delta > 0 else ("➖" if delta < 0 else "✅")
            output += "#### 👥 Resource Forecast (Linear Regression)\n"
            output += f"- **Current Team:** {data['current_ftes']} FTEs\n"
            output += f"- **Recommended:** {data['required_ftes']:.1f} FTEs\n"
            output += f"- **Delta:** {delta_emoji} {delta:+.1f}\n\n"
            
            # Burn Rate
            burn_emoji = "🔴" if data['burn_variance'] > 10 else ("🟡" if data['burn_variance'] > 0 else "🟢")
            output += "#### 🔥 Burn Rate Forecast (XGBoost)\n"
            output += f"- **Variance:** {burn_emoji} {data['burn_variance']:+.1f}%\n\n"
            
            output += "---\n\n"
        
        # Feature Importance
        output += "### 🎯 Feature Importance (Model Insights)\n\n"
        output += "**Cost Model Drivers:**\n"
        output += "- CPI: ███████ 35%\n"
        output += "- SPI: ████ 20%\n"
        output += "- Risk Score: ███ 15%\n"
        output += "- Blockers: ██ 12%\n\n"
        
        output += "**Schedule Model Drivers:**\n"
        output += "- SPI: ████████ 40%\n"
        output += "- Blockers: ████ 20%\n"
        output += "- Velocity Trend: ███ 15%\n"
        output += "- Team Utilization: ██ 12%\n"
        
        return output

    def _workflow_automation_agent(self) -> str:
        """Generate workflow analysis report."""
        output = "# ⚙️ Workflow Automation Agent\n\n"
        output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        output += get_workflow_status()
        
        output += "\n### 💡 AI Automation Recommendations\n\n"
        output += "1. **Automated Alerts:** Set up notifications for blockers > 3 days\n"
        output += "2. **WIP Limits:** Enforce WIP limits to improve flow efficiency\n"
        output += "3. **Status Updates:** Automate daily status collection from JIRA\n"
        output += "4. **Quality Gates:** Implement automated testing before deployments\n"
        output += "5. **Report Generation:** Schedule weekly automated status reports\n"
        
        return output

    def _default_response(self, query: str) -> str:
        """Default response for unrecognized queries."""
        return f"""# 🤖 PMO CoPilot

I'm your AI-First Project Management Assistant. I can help you with:

## Available Commands

| Command | Description |
|---------|-------------|
| `portfolio` | Get portfolio overview |
| `status [PROJECT]` | Generate status report |
| `risks [PROJECT]` | Analyze project risks |
| `evm [PROJECT]` | Earned Value Management analysis |
| `escalate [PROJECT]` | Generate escalation report |
| `rag` | RAG dashboard |
| `steerco` | Prepare SteerCo materials |
| `blockers [PROJECT]` | View blockers |
| `sprint [PROJECT]` | Sprint status |
| `schedule [PROJECT]` | Schedule optimization analysis |
| `resource [PROJECT]` | Resource allocation analysis |
| `milestone [PROJECT]` | Milestone tracking |
| `predict [PROJECT]` | Predictive analytics |
| `workflow` | Workflow efficiency analysis |

## Available Projects
- **ECOM** - E-Commerce Platform Migration (🟡 AMBER)
- **MAPP** - Customer Mobile App v2.0 (🟢 GREEN)
- **DPLAT** - Data Platform Modernization (🔴 RED)
- **SECU** - SOC2 Compliance Initiative (🟢 GREEN)

Try asking: "{query}" with a specific project or command!
"""

def run_demo():
    """Run interactive demo."""
    demo = PMOCoPilotDemo()

    print("=" * 70)
    print("🚀 PMO CoPilot Demo - AI-First Project Management Assistant")
    print("=" * 70)
    print("\nThis demo runs without OpenAI API keys.")
    print("Type 'help' for available commands, 'quit' to exit.\n")

    while True:
        query = input("📝 You: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break

        if not query:
            continue

        response = demo.process_query(query)
        print(f"\n🤖 PMO CoPilot:\n{response}\n")

if __name__ == "__main__":
    run_demo()
