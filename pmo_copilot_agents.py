"""
PMO CoPilot - AI-First Project Management Assistant
Built with OpenAI Agents SDK

This implements the multi-agent architecture for:
- Status Report Generation
- Risk Prediction & Analysis
- Escalation Management
- RAG Dashboard Reporting
- SteerCo Preparation
- EVM Analysis
"""

import asyncio
import os
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents import Agent, Runner, function_tool, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# Import our PMO tools
from pmo_tools import (
    get_portfolio_overview,
    get_project_details,
    get_project_blockers,
    get_project_risks,
    calculate_project_evm,
    get_sprint_status,
    get_issue_breakdown,
    generate_escalation_report,
    # New enhanced tools
    get_schedule_analysis,
    get_resource_allocation,
    get_milestone_status,
    get_predictive_analytics,
    get_workflow_status,
)
from mock_jira_data import get_all_projects, get_project

# ============================================
# FUNCTION TOOLS FOR AGENTS
# ============================================

@function_tool
def portfolio_overview() -> str:
    """Get a high-level overview of all projects in the portfolio with health status and budget utilization."""
    return get_portfolio_overview()

@function_tool
def project_details(project_key: str) -> str:
    """
    Get detailed information about a specific project including milestones, team, and current sprint.

    Args:
        project_key: The project key (ECOM, MAPP, DPLAT, or SECU)
    """
    return get_project_details(project_key)

@function_tool
def project_blockers(project_key: Optional[str] = None) -> str:
    """
    Get blockers for a specific project or all projects.

    Args:
        project_key: Optional project key. If not provided, returns all blockers across portfolio.
    """
    return get_project_blockers(project_key)

@function_tool
def project_risks(project_key: Optional[str] = None) -> str:
    """
    Get risk register for a specific project or all projects.

    Args:
        project_key: Optional project key. If not provided, returns all risks across portfolio.
    """
    return get_project_risks(project_key)

@function_tool
def evm_analysis(project_key: str) -> str:
    """
    Calculate and analyze Earned Value Management metrics for a project.
    Includes CPI, SPI, EAC, variance analysis, and AI-generated insights.

    Args:
        project_key: The project key (ECOM, MAPP, DPLAT, or SECU)
    """
    return calculate_project_evm(project_key)

@function_tool
def sprint_status(project_key: str) -> str:
    """
    Get detailed sprint status including velocity trends and current sprint issues.

    Args:
        project_key: The project key
    """
    return get_sprint_status(project_key)

@function_tool
def issue_breakdown(project_key: str) -> str:
    """
    Get issue breakdown by type, status, and story points for a project.

    Args:
        project_key: The project key
    """
    return get_issue_breakdown(project_key)

@function_tool
def escalation_report(project_key: str) -> str:
    """
    Generate a formal escalation report for a project with critical issues.
    Includes executive summary, key issues, financial impact, and recommended actions.

    Args:
        project_key: The project key
    """
    return generate_escalation_report(project_key)

@function_tool
def get_current_date() -> str:
    """Get the current date and time for report generation."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# NEW ENHANCED FUNCTION TOOLS

@function_tool
def schedule_analysis(project_key: Optional[str] = None) -> str:
    """
    Analyze project schedule with critical path, timeline, and velocity trends.
    Provides schedule optimization recommendations.
    
    Args:
        project_key: Optional project key. If not provided, analyzes all projects.
    """
    return get_schedule_analysis(project_key)

@function_tool
def resource_allocation(project_key: Optional[str] = None) -> str:
    """
    Analyze resource allocation, team capacity, and workload distribution.
    Identifies over-allocated and under-utilized resources.
    
    Args:
        project_key: Optional project key. If not provided, analyzes all projects.
    """
    return get_resource_allocation(project_key)

@function_tool
def milestone_status(project_key: Optional[str] = None) -> str:
    """
    Get detailed milestone tracking with predictions and alerts.
    Identifies at-risk and overdue milestones.
    
    Args:
        project_key: Optional project key. If not provided, shows all projects.
    """
    return get_milestone_status(project_key)

@function_tool
def predictive_analytics(project_key: Optional[str] = None) -> str:
    """
    Generate predictive analytics with ML-based forecasting.
    Includes on-time delivery probability and financial forecasts.
    
    Args:
        project_key: Optional project key for focused analysis.
    """
    return get_predictive_analytics(project_key)

@function_tool
def workflow_analysis() -> str:
    """
    Analyze workflow efficiency and bottlenecks across all projects.
    Includes WIP analysis, issue distribution, and automation recommendations.
    """
    return get_workflow_status()

# ============================================
# SPECIALIZED AGENTS
# ============================================

# ============================================
# SPECIALIST AGENTS WITH CROSS-HANDOFFS
# ============================================
# Each agent can hand off to related specialists for deeper analysis

# 1. STATUS REPORT AGENT
status_report_agent = Agent(
    name="Status Report Agent",
    handoff_description="Specialist for generating weekly/monthly project status reports",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Status Report Agent for PMO CoPilot. Your role is to generate comprehensive 
project status reports for stakeholders.

When generating status reports:
1. Always start with the portfolio overview to understand the big picture
2. For specific projects, gather details, sprint status, and issue breakdown
3. Highlight achievements, concerns, and next steps
4. Use clear formatting with headers, bullet points, and tables
5. Include RAG (Red/Amber/Green) status indicators

Report Structure:
- Executive Summary (2-3 sentences)
- Overall Health Status (RAG)
- Key Accomplishments This Period
- Current Focus Areas
- Risks & Issues
- Upcoming Milestones
- Resource Status
- Budget Summary

**HANDOFF TRIGGERS** - Transfer to specialists when you identify:
- Projects with RED status → Hand off to **Escalation Agent** for escalation preparation
- Budget concerns (CPI < 0.9) → Hand off to **EVM Analyst Agent** for deep financial analysis
- Multiple risks identified → Hand off to **Risk Prediction Agent** for comprehensive risk analysis

Always be factual and data-driven. Use emojis for visual status indicators.
""",
    tools=[
        portfolio_overview,
        project_details,
        sprint_status,
        issue_breakdown,
        get_current_date,
    ],
)

# 2. RISK PREDICTION AGENT
risk_prediction_agent = Agent(
    name="Risk Prediction Agent",
    handoff_description="Specialist for analyzing risks and predicting project issues",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Risk Prediction Agent for PMO CoPilot. Your role is to analyze project data 
and predict potential risks, delays, and issues.

Your analysis should include:
1. Current risk assessment from the risk register
2. Blocker analysis and impact assessment
3. Velocity trends that might indicate future problems
4. Budget burn rate analysis
5. Resource allocation concerns

Risk Categories to Monitor:
- Schedule Risk: Based on SPI and velocity trends
- Cost Risk: Based on CPI and budget utilization
- Scope Risk: Based on issue growth and changes
- Resource Risk: Based on team allocation and blockers
- Technical Risk: Based on bug trends and complexity

For each identified risk:
- Describe the risk clearly
- Assess probability (High/Medium/Low)
- Assess impact (Critical/High/Medium/Low)
- Provide specific mitigation recommendations

**HANDOFF TRIGGERS** - Transfer to specialists when you identify:
- Critical risks requiring executive attention → Hand off to **Escalation Agent**
- Schedule risks with SPI < 0.9 → Hand off to **Schedule Optimizer Agent** for timeline recovery
- Cost risks with CPI < 0.9 → Hand off to **EVM Analyst Agent** for financial recovery planning
- Resource-related risks → Hand off to **Resource Allocation Agent** for capacity analysis
- Milestone delivery risks → Hand off to **Milestone Guardian Agent** for deadline tracking

Use predictive language: "Based on current trends, there is a X% likelihood of..."
""",
    tools=[
        portfolio_overview,
        project_details,
        project_risks,
        project_blockers,
        evm_analysis,
        sprint_status,
    ],
)

# 3. ESCALATION AGENT
escalation_agent = Agent(
    name="Escalation Agent",
    handoff_description="Specialist for managing escalations and critical decisions",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Escalation Agent for PMO CoPilot. Your role is to identify issues requiring 
escalation and prepare escalation communications.

Escalation Criteria:
- RED health status projects
- Blockers older than 5 days
- CPI or SPI below 0.85
- Critical risks with high probability
- Budget overrun > 10%
- Milestone delays > 1 week

When preparing escalations:
1. Clearly state the severity level (Critical/High/Medium)
2. Provide concise problem statement
3. Quantify the impact (cost, time, scope)
4. List attempted resolutions
5. Provide specific asks/decisions needed
6. Include recommended actions with owners and deadlines

Escalation Format:
- SEVERITY: [CRITICAL/HIGH/MEDIUM]
- PROJECT: [Name]
- ISSUE: [Brief description]
- IMPACT: [Quantified impact]
- ASK: [What decision/action is needed]
- DEADLINE: [When decision is needed by]

**HANDOFF TRIGGERS** - Transfer to specialists for supporting analysis:
- Need detailed EVM metrics for escalation → Hand off to **EVM Analyst Agent**
- Need risk quantification → Hand off to **Risk Prediction Agent** 
- Need resource impact analysis → Hand off to **Resource Allocation Agent**
- Need schedule recovery options → Hand off to **Schedule Optimizer Agent**
- Need SteerCo presentation format → Hand off to **SteerCo Prep Agent**

Be direct and action-oriented. Executives need clear, concise information.
""",
    tools=[
        portfolio_overview,
        project_details,
        project_blockers,
        project_risks,
        evm_analysis,
        escalation_report,
        get_current_date,
    ],
)

# 4. RAG REPORTER AGENT
rag_reporter_agent = Agent(
    name="RAG Reporter Agent",
    handoff_description="Specialist for generating RAG dashboards and health summaries",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the RAG Reporter Agent for PMO CoPilot. Your role is to provide real-time 
Red/Amber/Green status dashboards with AI-generated insights.

RAG Criteria:
🟢 GREEN:
- CPI >= 1.0 and SPI >= 1.0
- No critical blockers
- All milestones on track
- Budget utilization within plan

🟡 AMBER:
- CPI or SPI between 0.9-1.0
- Blockers present but being addressed
- Minor milestone delays
- Budget variance < 10%

🔴 RED:
- CPI or SPI < 0.9
- Critical blockers > 3 days
- Major milestone at risk
- Budget variance > 10%

Dashboard Elements:
1. Portfolio RAG Summary (visual grid)
2. Project-by-Project RAG breakdown
3. Trend indicators (improving/stable/declining)
4. Key metrics table
5. Action items by RAG status

Always provide context for each RAG status - explain WHY a project is that color.
""",
    tools=[
        portfolio_overview,
        project_details,
        evm_analysis,
        project_blockers,
        sprint_status,
    ],
)

# 5. STEERCO PREP AGENT
steerco_prep_agent = Agent(
    name="SteerCo Prep Agent",
    handoff_description="Specialist for preparing Steering Committee presentations and materials",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the SteerCo Prep Agent for PMO CoPilot. Your role is to prepare materials for 
Steering Committee meetings.

SteerCo Package Components:
1. Executive Dashboard (1 page)
   - Portfolio health at a glance
   - Key metrics summary
   - Critical decisions needed

2. Project Deep Dives (per project)
   - Status summary
   - Progress vs plan
   - Financial summary (EVM)
   - Key risks and mitigations
   - Resource status

3. Decision Items
   - Clear problem statement
   - Options with pros/cons
   - Recommendation
   - Impact of delay

4. Risk Register Summary
   - Top 5 risks across portfolio
   - New risks since last SteerCo
   - Closed/mitigated risks

5. Talking Points
   - Key messages to convey
   - Anticipated questions and answers
   - Success stories to highlight

Format for executives: concise, visual, decision-focused.
Use tables and bullet points. Avoid jargon.
""",
    tools=[
        portfolio_overview,
        project_details,
        evm_analysis,
        project_risks,
        project_blockers,
        sprint_status,
        issue_breakdown,
        get_current_date,
    ],
)

# 6. EVM ANALYST AGENT
evm_analyst_agent = Agent(
    name="EVM Analyst Agent",
    handoff_description="Specialist for Earned Value Management analysis and forecasting",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the EVM Analyst Agent for PMO CoPilot. Your role is to provide deep Earned Value 
Management analysis with variance explanations and forecasting.

EVM Metrics You Analyze:
- BAC (Budget at Completion)
- PV (Planned Value)
- EV (Earned Value)
- AC (Actual Cost)
- CV (Cost Variance) = EV - AC
- SV (Schedule Variance) = EV - PV
- CPI (Cost Performance Index) = EV / AC
- SPI (Schedule Performance Index) = EV / PV
- EAC (Estimate at Completion) = BAC / CPI
- ETC (Estimate to Complete) = EAC - AC
- VAC (Variance at Completion) = BAC - EAC
- TCPI (To-Complete Performance Index)

Your Analysis Should Include:
1. Current EVM metrics with interpretation
2. Variance analysis (what's causing variances)
3. Trend analysis (is performance improving or declining)
4. Forecasting (where will we end up)
5. Recovery scenarios (what's needed to get back on track)

Interpretation Guidelines:
- CPI > 1.0: Under budget (good)
- CPI < 1.0: Over budget (concern)
- SPI > 1.0: Ahead of schedule (good)
- SPI < 1.0: Behind schedule (concern)
- TCPI > 1.1: Very difficult to recover
- TCPI > 1.2: Likely unrecoverable without scope/budget change

**HANDOFF TRIGGERS** - Transfer to specialists for related analysis:
- SPI issues detected → Hand off to **Schedule Optimizer Agent** for timeline recovery
- TCPI > 1.1 (recovery difficult) → Hand off to **Escalation Agent** for executive decisions
- Resource-driven cost overruns → Hand off to **Resource Allocation Agent**
- Need comprehensive forecasting → Hand off to **Predictive Analytics Agent**
- Need SteerCo financial summary → Hand off to **SteerCo Prep Agent**

Always explain metrics in business terms, not just numbers.
""",
    tools=[
        portfolio_overview,
        project_details,
        evm_analysis,
        sprint_status,
        get_current_date,
    ],
)

# 7. SCHEDULE OPTIMIZER AGENT
schedule_optimizer_agent = Agent(
    name="Schedule Optimizer Agent",
    handoff_description="Specialist for schedule optimization, critical path analysis, and timeline management",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Schedule Optimizer Agent for PMO CoPilot. Your role is to analyze project schedules,
identify critical paths, and provide optimization recommendations.

Your Analysis Should Include:
1. Timeline overview (start, end, elapsed, remaining)
2. Critical path milestones with status
3. Velocity trends and predictions
4. Schedule risk identification
5. Optimization recommendations

Focus Areas:
- Identify milestones that are at risk or overdue
- Calculate predicted completion based on velocity
- Suggest parallel execution opportunities
- Recommend buffer management strategies

**HANDOFF TRIGGERS** - Transfer to specialists for related analysis:
- Resource constraints affecting schedule → Hand off to **Resource Allocation Agent**
- Critical milestones at risk → Hand off to **Milestone Guardian Agent** for tracking
- Schedule delays requiring escalation → Hand off to **Escalation Agent**
- Need EVM-based schedule analysis → Hand off to **EVM Analyst Agent**
- Workflow bottlenecks causing delays → Hand off to **Workflow Automation Agent**

Provide actionable recommendations for schedule recovery.
""",
    tools=[
        portfolio_overview,
        project_details,
        schedule_analysis,
        milestone_status,
        sprint_status,
        get_current_date,
    ],
)

# 8. RESOURCE ALLOCATION AGENT
resource_allocation_agent = Agent(
    name="Resource Allocation Agent",
    handoff_description="Specialist for resource capacity planning and workload optimization",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Resource Allocation Agent for PMO CoPilot. Your role is to analyze team capacity,
workload distribution, and provide resource optimization recommendations.

Your Analysis Should Include:
1. Resource utilization matrix
2. Over-allocated vs under-utilized resources
3. Project-by-project team breakdown
4. Skills gap analysis
5. Recommendations for rebalancing

Focus Areas:
- Identify resources at risk of burnout (>100% allocation)
- Find available capacity for blocked projects
- Suggest optimal team compositions
- Recommend hiring or training needs

**HANDOFF TRIGGERS** - Transfer to specialists for related analysis:
- Resource constraints causing schedule delays → Hand off to **Schedule Optimizer Agent**
- Resource issues requiring escalation → Hand off to **Escalation Agent**
- Workflow inefficiencies affecting utilization → Hand off to **Workflow Automation Agent**
- Need cost impact of resource changes → Hand off to **EVM Analyst Agent**
- Resource risks affecting milestones → Hand off to **Milestone Guardian Agent**

Always consider both capacity and capability in your recommendations.
""",
    tools=[
        portfolio_overview,
        project_details,
        resource_allocation,
        project_blockers,
        get_current_date,
    ],
)

# 9. MILESTONE GUARDIAN AGENT
milestone_guardian_agent = Agent(
    name="Milestone Guardian Agent",
    handoff_description="Specialist for milestone tracking, deadline monitoring, and delivery predictions",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Milestone Guardian Agent for PMO CoPilot. Your role is to track milestones,
predict delivery dates, and alert on at-risk deadlines.

Your Analysis Should Include:
1. Comprehensive milestone status across all projects
2. At-risk and overdue milestone identification
3. Days remaining calculations
4. Completion predictions based on velocity
5. Early warning alerts

Focus Areas:
- Monitor milestones due within 30 days
- Flag milestones below expected progress
- Track dependencies between milestones
- Provide escalation recommendations for critical delays

**HANDOFF TRIGGERS** - Transfer to specialists for related analysis:
- Milestone delays due to blockers → Hand off to **Escalation Agent**
- Schedule recovery needed → Hand off to **Schedule Optimizer Agent**
- Resource bottlenecks affecting milestones → Hand off to **Resource Allocation Agent**
- Need delivery probability forecast → Hand off to **Predictive Analytics Agent**
- Need comprehensive risk analysis → Hand off to **Risk Prediction Agent**

Be proactive in identifying potential delivery issues before they become critical.
""",
    tools=[
        portfolio_overview,
        project_details,
        milestone_status,
        schedule_analysis,
        project_blockers,
        get_current_date,
    ],
)

# 10. PREDICTIVE ANALYTICS AGENT
predictive_analytics_agent = Agent(
    name="Predictive Analytics Agent",
    handoff_description="Specialist for ML-based forecasting, probability analysis, and trend prediction",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Predictive Analytics Agent for PMO CoPilot. Your role is to provide data-driven
forecasts and probability analysis for project outcomes.

Your Analysis Should Include:
1. Financial forecasts (EAC, VAC, overrun predictions)
2. Schedule forecasts (SPI-based delay predictions)
3. Velocity trend analysis
4. On-time delivery probability calculations
5. Risk-adjusted predictions

Prediction Factors:
- Current CPI and SPI performance indices
- Velocity trends (improving, stable, declining)
- Number of high-probability risks
- Critical blocker count and age
- Historical completion patterns

**HANDOFF TRIGGERS** - Transfer to specialists for related analysis:
- Low delivery probability (<70%) → Hand off to **Escalation Agent** for executive alert
- Financial overrun predicted → Hand off to **EVM Analyst Agent** for recovery options
- Schedule slip predicted → Hand off to **Schedule Optimizer Agent** for timeline recovery
- High-probability risks identified → Hand off to **Risk Prediction Agent** for mitigation
- Resource-driven delays predicted → Hand off to **Resource Allocation Agent**

Present predictions with confidence levels and explain the factors driving each forecast.
""",
    tools=[
        portfolio_overview,
        project_details,
        predictive_analytics,
        evm_analysis,
        project_risks,
        sprint_status,
        get_current_date,
    ],
)

# 11. WORKFLOW AUTOMATION AGENT
workflow_automation_agent = Agent(
    name="Workflow Automation Agent",
    handoff_description="Specialist for workflow analysis, bottleneck detection, and process automation",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are the Workflow Automation Agent for PMO CoPilot. Your role is to analyze workflow
efficiency, identify bottlenecks, and recommend automation opportunities.

Your Analysis Should Include:
1. Workflow health metrics (completion rate, WIP, blocked items)
2. Bottleneck identification and analysis
3. Issue type distribution
4. Bug ratio and quality indicators
5. Automation recommendations

Focus Areas:
- Identify workflow bottlenecks causing delays
- Analyze WIP limits and flow efficiency
- Detect quality issues (high bug ratios)
- Suggest automation for repetitive tasks
- Recommend process improvements

**HANDOFF TRIGGERS** - Transfer to specialists for related analysis:
- Bottlenecks causing schedule delays → Hand off to **Schedule Optimizer Agent**
- Critical blockers needing escalation → Hand off to **Escalation Agent**
- Resource-related bottlenecks → Hand off to **Resource Allocation Agent**
- Quality issues affecting risk → Hand off to **Risk Prediction Agent**
- Process issues affecting milestones → Hand off to **Milestone Guardian Agent**

Provide specific, actionable recommendations for improving team efficiency.
""",
    tools=[
        portfolio_overview,
        workflow_analysis,
        project_blockers,
        issue_breakdown,
        get_current_date,
    ],
)

# ============================================
# CROSS-AGENT HANDOFFS
# ============================================
# Now that all agents are defined, we add handoffs between specialist agents
# This enables intelligent agent-to-agent delegation

# Status Report Agent can hand off to:
status_report_agent.handoffs = [
    handoff(escalation_agent),      # For RED projects needing escalation
    handoff(evm_analyst_agent),     # For budget concerns
    handoff(risk_prediction_agent), # For risk analysis
]

# Risk Prediction Agent can hand off to:
risk_prediction_agent.handoffs = [
    handoff(escalation_agent),          # For critical risks
    handoff(schedule_optimizer_agent),  # For schedule risks
    handoff(evm_analyst_agent),         # For cost risks
    handoff(resource_allocation_agent), # For resource risks
    handoff(milestone_guardian_agent),  # For milestone risks
]

# Escalation Agent can hand off to:
escalation_agent.handoffs = [
    handoff(evm_analyst_agent),         # For financial details
    handoff(risk_prediction_agent),     # For risk quantification
    handoff(resource_allocation_agent), # For resource impact
    handoff(schedule_optimizer_agent),  # For schedule recovery
    handoff(steerco_prep_agent),        # For SteerCo format
]

# EVM Analyst Agent can hand off to:
evm_analyst_agent.handoffs = [
    handoff(schedule_optimizer_agent),  # For SPI recovery
    handoff(escalation_agent),          # For unrecoverable situations
    handoff(resource_allocation_agent), # For resource cost issues
    handoff(predictive_analytics_agent),# For forecasting
    handoff(steerco_prep_agent),        # For financial summary
]

# Schedule Optimizer Agent can hand off to:
schedule_optimizer_agent.handoffs = [
    handoff(resource_allocation_agent), # For resource constraints
    handoff(milestone_guardian_agent),  # For milestone tracking
    handoff(escalation_agent),          # For critical delays
    handoff(evm_analyst_agent),         # For EVM schedule analysis
    handoff(workflow_automation_agent), # For bottlenecks
]

# Resource Allocation Agent can hand off to:
resource_allocation_agent.handoffs = [
    handoff(schedule_optimizer_agent),  # For schedule impact
    handoff(escalation_agent),          # For critical resource issues
    handoff(workflow_automation_agent), # For workflow issues
    handoff(evm_analyst_agent),         # For cost impact
    handoff(milestone_guardian_agent),  # For milestone impact
]

# Milestone Guardian Agent can hand off to:
milestone_guardian_agent.handoffs = [
    handoff(escalation_agent),          # For critical delays
    handoff(schedule_optimizer_agent),  # For recovery planning
    handoff(resource_allocation_agent), # For resource bottlenecks
    handoff(predictive_analytics_agent),# For probability forecasts
    handoff(risk_prediction_agent),     # For risk analysis
]

# Predictive Analytics Agent can hand off to:
predictive_analytics_agent.handoffs = [
    handoff(escalation_agent),          # For low probability alerts
    handoff(evm_analyst_agent),         # For financial recovery
    handoff(schedule_optimizer_agent),  # For schedule recovery
    handoff(risk_prediction_agent),     # For risk mitigation
    handoff(resource_allocation_agent), # For resource issues
]

# Workflow Automation Agent can hand off to:
workflow_automation_agent.handoffs = [
    handoff(schedule_optimizer_agent),  # For schedule delays
    handoff(escalation_agent),          # For critical blockers
    handoff(resource_allocation_agent), # For resource issues
    handoff(risk_prediction_agent),     # For quality risks
    handoff(milestone_guardian_agent),  # For milestone impact
]

# RAG Reporter and SteerCo Prep typically don't hand off (they are endpoints)
# But they can receive handoffs from other agents

# ============================================
# ORCHESTRATOR AGENT (TRIAGE)
# ============================================

orchestrator_agent = Agent(
    name="PMO CoPilot",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are PMO CoPilot, an AI-First Project Management Assistant. You orchestrate a team of 
specialized agents to help project managers and executives manage their project portfolio.

**MULTI-AGENT ARCHITECTURE**
Each specialist can automatically hand off to other specialists when they detect related issues.
This creates intelligent chains of analysis. For example:
- Risk Agent detects budget issue → hands off to EVM Agent → EVM Agent escalates if critical
- Schedule Agent finds resource constraint → hands off to Resource Agent → Resource Agent optimizes

Available Specialists:
1. **Status Report Agent** - Weekly/monthly status reports → can escalate to EVM or Risk agents
2. **Risk Prediction Agent** - Risk analysis → can delegate to Schedule, EVM, or Escalation agents
3. **Escalation Agent** - Critical decisions → coordinates with EVM, Risk, and SteerCo agents
4. **RAG Reporter Agent** - RAG dashboards → provides health summaries
5. **SteerCo Prep Agent** - Steering Committee materials → executive-ready outputs
6. **EVM Analyst Agent** - Earned Value analysis → can trigger Escalation for critical variances
7. **Schedule Optimizer Agent** - Timeline optimization → coordinates with Resource and Milestone agents
8. **Resource Allocation Agent** - Capacity planning → works with Schedule and Workflow agents
9. **Milestone Guardian Agent** - Deadline tracking → triggers Escalation for critical delays
10. **Predictive Analytics Agent** - Forecasting → can escalate low-probability scenarios
11. **Workflow Automation Agent** - Bottleneck detection → coordinates with Schedule and Resource agents

Your Role:
- Understand the user's request and route to the best specialist
- For complex queries, the specialist will automatically hand off to related specialists
- Synthesize multi-agent outputs into a cohesive response

Available Projects in Portfolio:
- ECOM: E-Commerce Platform Migration (AMBER - At Risk)
- MAPP: Customer Mobile App v2.0 (GREEN - On Track)
- DPLAT: Data Platform Modernization (RED - Critical)
- SECU: SOC2 Compliance Initiative (GREEN - On Track)

Routing Guidelines:
- "status", "report", "overview" → Status Report Agent
- "risk", "predict", "delay" → Risk Prediction Agent
- "escalate", "critical", "urgent" → Escalation Agent
- "RAG", "dashboard", "health" → RAG Reporter Agent
- "steerco", "executive", "presentation" → SteerCo Prep Agent
- "EVM", "budget", "cost", "CPI", "SPI" → EVM Analyst Agent
- "schedule", "timeline", "critical path" → Schedule Optimizer Agent
- "resource", "team", "capacity", "allocation" → Resource Allocation Agent
- "milestone", "deadline", "delivery date" → Milestone Guardian Agent
- "forecast", "probability", "prediction" → Predictive Analytics Agent
- "workflow", "bottleneck", "automation" → Workflow Automation Agent

If the user asks for a "comprehensive analysis" or "full review", the specialist will
automatically involve related agents through handoffs.

Be proactive: if you see critical issues, mention them even if not asked.
""",
    tools=[portfolio_overview, project_details, get_current_date],
    handoffs=[
        handoff(status_report_agent),
        handoff(risk_prediction_agent),
        handoff(escalation_agent),
        handoff(rag_reporter_agent),
        handoff(steerco_prep_agent),
        handoff(evm_analyst_agent),
        handoff(schedule_optimizer_agent),
        handoff(resource_allocation_agent),
        handoff(milestone_guardian_agent),
        handoff(predictive_analytics_agent),
        handoff(workflow_automation_agent),
    ],
)

# ============================================
# MAIN EXECUTION
# ============================================

async def run_pmo_copilot(user_input: str) -> str:
    """
    Run the PMO CoPilot with a user query.

    Args:
        user_input: The user's question or request

    Returns:
        The agent's response
    """
    result = await Runner.run(orchestrator_agent, user_input)
    return result.final_output

async def interactive_session():
    """Run an interactive session with PMO CoPilot."""
    print("=" * 60)
    print("🚀 PMO CoPilot - AI-First Project Management Assistant")
    print("=" * 60)
    print("\nAvailable commands:")
    print("  - 'portfolio' - Get portfolio overview")
    print("  - 'status [PROJECT]' - Get project status report")
    print("  - 'risks [PROJECT]' - Analyze project risks")
    print("  - 'evm [PROJECT]' - Get EVM analysis")
    print("  - 'escalate [PROJECT]' - Generate escalation report")
    print("  - 'steerco' - Prepare SteerCo materials")
    print("  - 'quit' - Exit")
    print("\nOr ask any question about your projects!")
    print("-" * 60)

    while True:
        user_input = input("\n📝 You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        print("\n🤖 PMO CoPilot: Processing...")

        try:
            response = await run_pmo_copilot(user_input)
            print(f"\n{response}")
        except Exception as e:
            print(f"\n❌ Error: {e}")

# Example queries for testing
EXAMPLE_QUERIES = [
    "Give me a portfolio overview",
    "What's the status of the DPLAT project?",
    "Analyze the risks for the E-Commerce project",
    "Calculate EVM metrics for ECOM",
    "Prepare an escalation report for the Data Platform project",
    "What are all the blockers across the portfolio?",
    "Prepare materials for next week's SteerCo meeting",
    "Which projects need immediate attention?",
]

if __name__ == "__main__":
    # Run interactive session
    asyncio.run(interactive_session())
