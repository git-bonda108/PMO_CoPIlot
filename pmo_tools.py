"""
PMO CoPilot - Function Tools for OpenAI Agents SDK
Enhanced with Schedule, Resource, Milestone, and Predictive Analytics
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from mock_jira_data import (
    get_project, get_all_projects, get_project_summary,
    get_all_blockers, get_all_risks, ALL_PROJECTS
)
from evm_calculator import calculate_evm, format_evm_report, get_evm_insights


def get_portfolio_overview() -> str:
    """Get a high-level overview of all projects in the portfolio."""
    summaries = get_project_summary()
    output = "## Portfolio Overview\n\n"
    output += "| Project | PM | Health | Status | Budget | Spent | Utilization |\n"
    output += "|---------|-----|--------|--------|--------|-------|-------------|\n"
    for s in summaries:
        health_emoji = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}.get(s["health"], "⚪")
        output += f"| {s['project_name']} | {s['project_manager']} | {health_emoji} {s['health']} | {s['status']} | \${s['budget']:,} | \${s['spent']:,} | {s['budget_utilization']}% |\n"
    total_budget = sum(s["budget"] for s in summaries)
    total_spent = sum(s["spent"] for s in summaries)
    red_projects = sum(1 for s in summaries if s["health"] == "RED")
    amber_projects = sum(1 for s in summaries if s["health"] == "AMBER")
    output += f"\n### Portfolio Summary\n"
    output += f"- **Total Budget:** \${total_budget:,}\n"
    output += f"- **Total Spent:** \${total_spent:,} ({total_spent/total_budget*100:.1f}%)\n"
    output += f"- **Projects at Risk:** {red_projects} RED, {amber_projects} AMBER\n"
    return output


def get_project_details(project_key: str) -> str:
    """Get detailed information about a specific project."""
    project = get_project(project_key.upper())
    if not project:
        return f"Project {project_key} not found. Available: ECOM, MAPP, DPLAT, SECU"
    output = f"## {project['project_name']}\n\n"
    output += f"**Project Manager:** {project['project_manager']}\n"
    output += f"**Status:** {project['status']} | **Health:** {project['health']}\n"
    output += f"**Timeline:** {project['start_date']} to {project['planned_end_date']}\n"
    output += f"**Budget:** \${project['budget']:,} | **Spent:** \${project['spent']:,}\n\n"
    output += "### Milestones\n"
    for m in project["milestones"]:
        status_emoji = {"COMPLETED": "✅", "ON_TRACK": "🟢", "AT_RISK": "🟡", "NOT_STARTED": "⬜"}.get(m["status"], "❓")
        output += f"- {status_emoji} **{m['name']}** - Due: {m['due_date']} ({m['completion']}% complete)\n"
    output += "\n### Team\n"
    for t in project["team"]:
        output += f"- {t['name']} ({t['role']}) - {t['allocation']}% allocated\n"
    current_sprint = next((s for s in project["sprints"] if s["status"] == "IN_PROGRESS"), None)
    if current_sprint:
        output += f"\n### Current Sprint\n"
        output += f"**{current_sprint['name']}** - Velocity: {current_sprint['velocity']}\n"
    return output


def get_project_blockers(project_key: Optional[str] = None) -> str:
    """Get blockers for a specific project or all projects."""
    if project_key:
        project = get_project(project_key.upper())
        if not project:
            return f"Project {project_key} not found."
        blockers = project.get("blockers", [])
        project_name = project["project_name"]
    else:
        blockers = get_all_blockers()
        project_name = "All Projects"
    if not blockers:
        return f"No blockers found for {project_name}. 🎉"
    output = f"## Blockers - {project_name}\n\n"
    output += "| Issue | Description | Blocked Since | Impact |\n"
    output += "|-------|-------------|---------------|--------|\n"
    for b in blockers:
        impact_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(b["impact"], "⚪")
        proj = b.get("project_key", project_key or "")
        output += f"| [{proj}] {b['issue_key']} | {b['description']} | {b['blocked_since']} | {impact_emoji} {b['impact']} |\n"
    output += "\n### Blocker Age Analysis\n"
    today = datetime.now()
    for b in blockers:
        blocked_date = datetime.strptime(b["blocked_since"], "%Y-%m-%d")
        days_blocked = (today - blocked_date).days
        output += f"- **{b['issue_key']}**: Blocked for {days_blocked} days\n"
    return output


def get_project_risks(project_key: Optional[str] = None) -> str:
    """Get risks for a specific project or all projects."""
    if project_key:
        project = get_project(project_key.upper())
        if not project:
            return f"Project {project_key} not found."
        risks = project.get("risks", [])
        project_name = project["project_name"]
    else:
        risks = get_all_risks()
        project_name = "All Projects"
    output = f"## Risk Register - {project_name}\n\n"
    output += "| ID | Risk | Probability | Impact | Mitigation |\n"
    output += "|----|------|-------------|--------|------------|\n"
    for r in risks:
        prob_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(r["probability"], "⚪")
        impact_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(r["impact"], "⚪")
        proj = r.get("project_key", project_key or "")
        output += f"| [{proj}] {r['id']} | {r['description']} | {prob_emoji} {r['probability']} | {impact_emoji} {r['impact']} | {r['mitigation']} |\n"
    high_prob = sum(1 for r in risks if r["probability"] == "HIGH")
    critical_impact = sum(1 for r in risks if r["impact"] in ["CRITICAL", "HIGH"])
    output += f"\n### Risk Summary\n"
    output += f"- **High Probability Risks:** {high_prob}\n"
    output += f"- **Critical/High Impact Risks:** {critical_impact}\n"
    return output


def calculate_project_evm(project_key: str) -> str:
    """Calculate and return EVM metrics for a specific project."""
    project = get_project(project_key.upper())
    if not project:
        return f"Project {project_key} not found."
    evm_data = project.get("evm", {})
    if not evm_data:
        return f"No EVM data available for {project_key}"
    metrics = calculate_evm(evm_data)
    report = format_evm_report(metrics, project["project_name"])
    insights = get_evm_insights(metrics)
    output = report
    output += "\n### AI Insights\n"
    output += f"**Summary:** {insights['summary']}\n\n"
    if insights["concerns"]:
        output += "**Concerns:**\n"
        for c in insights["concerns"]:
            output += f"- ⚠️ {c}\n"
    if insights["recommendations"]:
        output += "\n**Recommendations:**\n"
        for r in insights["recommendations"]:
            output += f"- 💡 {r}\n"
    return output


def get_sprint_status(project_key: str) -> str:
    """Get detailed sprint status for a project."""
    project = get_project(project_key.upper())
    if not project:
        return f"Project {project_key} not found."
    output = f"## Sprint Status - {project['project_name']}\n\n"
    output += "### Sprint History\n"
    output += "| Sprint | Status | Velocity |\n"
    output += "|--------|--------|----------|\n"
    velocities = []
    for s in project["sprints"]:
        status_emoji = {"COMPLETED": "✅", "IN_PROGRESS": "🔄", "PLANNED": "📅", "BLOCKED": "🚫"}.get(s["status"], "❓")
        vel = s["velocity"] if s["velocity"] else "-"
        if s["velocity"]:
            velocities.append(s["velocity"])
        output += f"| {s['name']} | {status_emoji} {s['status']} | {vel} |\n"
    if len(velocities) >= 2:
        avg_velocity = sum(velocities) / len(velocities)
        trend = "📈 Increasing" if velocities[-1] > velocities[0] else "📉 Decreasing"
        output += f"\n### Velocity Analysis\n"
        output += f"- **Average Velocity:** {avg_velocity:.1f}\n"
        output += f"- **Trend:** {trend}\n"
    current_sprint = next((s for s in project["sprints"] if s["status"] == "IN_PROGRESS"), None)
    if current_sprint:
        output += f"\n### Current Sprint Issues\n"
        in_progress = [i for i in project["issues"] if i["status"] == "In Progress"]
        for issue in in_progress[:5]:
            priority_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(issue["priority"], "⚪")
            output += f"- [{issue['key']}] {issue['summary']} ({priority_emoji} {issue['priority']})\n"
    return output


def get_issue_breakdown(project_key: str) -> str:
    """Get issue breakdown by type and status for a project."""
    project = get_project(project_key.upper())
    if not project:
        return f"Project {project_key} not found."
    issues = project.get("issues", [])
    output = f"## Issue Breakdown - {project['project_name']}\n\n"
    types = {}
    for i in issues:
        t = i["type"]
        types[t] = types.get(t, 0) + 1
    output += "### By Type\n"
    for t, count in types.items():
        output += f"- **{t}:** {count}\n"
    statuses = {}
    for i in issues:
        s = i["status"]
        statuses[s] = statuses.get(s, 0) + 1
    output += "\n### By Status\n"
    for s, count in statuses.items():
        emoji = {"Done": "✅", "In Progress": "🔄", "To Do": "📋", "Open": "📂", "Blocked": "🚫"}.get(s, "❓")
        output += f"- {emoji} **{s}:** {count}\n"
    total_points = sum(i.get("story_points", 0) for i in issues)
    done_points = sum(i.get("story_points", 0) for i in issues if i["status"] == "Done")
    output += f"\n### Story Points\n"
    output += f"- **Total:** {total_points}\n"
    output += f"- **Completed:** {done_points} ({done_points/total_points*100:.1f}%)\n"
    critical = [i for i in issues if i["priority"] == "Critical" and i["status"] != "Done"]
    if critical:
        output += "\n### ⚠️ Open Critical Issues\n"
        for i in critical:
            output += f"- [{i['key']}] {i['summary']} - {i['status']}\n"
    return output


def generate_escalation_report(project_key: str) -> str:
    """Generate an escalation report for a project with critical issues."""
    project = get_project(project_key.upper())
    if not project:
        return f"Project {project_key} not found."
    output = f"# 🚨 ESCALATION REPORT\n## {project['project_name']}\n"
    output += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    output += f"**Project Manager:** {project['project_manager']}\n"
    output += f"**Current Status:** {project['status']} | **Health:** {project['health']}\n\n---\n\n"
    blockers = project.get("blockers", [])
    critical_risks = [r for r in project.get("risks", []) if r["probability"] == "HIGH" or r["impact"] in ["CRITICAL", "HIGH"]]
    if project["health"] == "RED":
        output += "## Executive Summary\n**SEVERITY: CRITICAL** - Immediate executive attention required.\n\n"
    elif project["health"] == "AMBER":
        output += "## Executive Summary\n**SEVERITY: HIGH** - Management attention required within 48 hours.\n\n"
    else:
        output += "## Executive Summary\n**SEVERITY: MODERATE** - Monitoring recommended.\n\n"
    output += "## Key Issues Requiring Escalation\n\n"
    if blockers:
        output += "### Active Blockers\n"
        for b in blockers:
            output += f"- **{b['issue_key']}**: {b['description']} (Impact: {b['impact']})\n"
    if critical_risks:
        output += "\n### Critical Risks\n"
        for r in critical_risks:
            output += f"- **{r['id']}**: {r['description']}\n"
    evm_data = project.get("evm", {})
    if evm_data:
        metrics = calculate_evm(evm_data)
        output += f"\n## Financial Impact\n"
        output += f"| Metric | Value |\n|--------|-------|\n"
        output += f"| Budget at Completion | \${metrics.BAC:,.0f} |\n"
        output += f"| Current Spend | \${metrics.AC:,.0f} |\n"
        output += f"| Projected Final Cost | \${metrics.EAC:,.0f} |\n"
    output += "\n## Recommended Actions\n"
    output += "1. Schedule emergency stakeholder meeting\n"
    output += "2. Assign dedicated resources to blockers\n"
    output += "3. Conduct root cause analysis\n"
    return output


# ============================================
# NEW ENHANCED TOOLS
# ============================================

def get_schedule_analysis(project_key: Optional[str] = None) -> str:
    """Analyze project schedule with dependencies and critical path."""
    if project_key:
        projects = [get_project(project_key.upper())]
        if not projects[0]:
            return f"Project {project_key} not found."
    else:
        projects = list(ALL_PROJECTS.values())
    
    output = "## 📅 Schedule Optimizer Report\n\n"
    
    for project in projects:
        if not project:
            continue
        output += f"### {project['project_name']} ({project['project_key']})\n\n"
        start = datetime.strptime(project['start_date'], "%Y-%m-%d")
        end = datetime.strptime(project['planned_end_date'], "%Y-%m-%d")
        today = datetime.now()
        total_days = (end - start).days
        elapsed_days = (today - start).days
        remaining_days = (end - today).days
        
        output += "**Timeline Overview:**\n"
        output += f"- Start: {project['start_date']} | End: {project['planned_end_date']}\n"
        output += f"- Total Duration: {total_days} days\n"
        output += f"- Days Elapsed: {elapsed_days} ({elapsed_days/total_days*100:.1f}%)\n"
        output += f"- Days Remaining: {remaining_days}\n\n"
        
        output += "**Critical Path - Milestones:**\n"
        milestones = project.get("milestones", [])
        for i, m in enumerate(milestones):
            status_emoji = {"COMPLETED": "✅", "ON_TRACK": "🟢", "AT_RISK": "🟡", "NOT_STARTED": "⬜"}.get(m["status"], "❓")
            output += f"{i+1}. {status_emoji} **{m['name']}** - Due: {m['due_date']} ({m['completion']}%)\n"
            if m['status'] not in ['COMPLETED', 'ON_TRACK']:
                due = datetime.strptime(m['due_date'], "%Y-%m-%d")
                if due < today:
                    output += f"   ⚠️ OVERDUE by {(today - due).days} days\n"
                elif (due - today).days < 14:
                    output += f"   ⚠️ Due in {(due - today).days} days\n"
        
        sprints = project.get("sprints", [])
        velocities = [s['velocity'] for s in sprints if s['velocity']]
        if len(velocities) >= 2:
            avg_velocity = sum(velocities) / len(velocities)
            recent_velocity = velocities[-1]
            trend = "📈 Improving" if recent_velocity > avg_velocity else "📉 Declining"
            output += f"\n**Velocity Trend:** {trend}\n"
            output += f"- Average: {avg_velocity:.1f} | Recent: {recent_velocity}\n"
            remaining_points = sum(i.get('story_points', 0) for i in project.get('issues', []) if i['status'] != 'Done')
            if recent_velocity > 0:
                sprints_needed = remaining_points / recent_velocity
                predicted_weeks = sprints_needed * 2
                output += f"- Remaining Story Points: {remaining_points}\n"
                output += f"- Predicted weeks to complete: {predicted_weeks:.1f}\n"
        output += "\n---\n\n"
    return output


def get_resource_allocation(project_key: Optional[str] = None) -> str:
    """Analyze resource allocation and capacity across projects."""
    if project_key:
        projects = {project_key.upper(): get_project(project_key.upper())}
        if not projects[project_key.upper()]:
            return f"Project {project_key} not found."
    else:
        projects = ALL_PROJECTS
    
    output = "## 👥 Resource Allocation Analysis\n\n"
    all_resources = {}
    for key, project in projects.items():
        if not project:
            continue
        for member in project.get("team", []):
            name = member['name']
            if name not in all_resources:
                all_resources[name] = {'role': member['role'], 'projects': [], 'total_allocation': 0}
            all_resources[name]['projects'].append({'project': key, 'allocation': member['allocation']})
            all_resources[name]['total_allocation'] += member['allocation']
    
    output += "### Resource Utilization Matrix\n\n"
    output += "| Resource | Role | Total Allocation | Status |\n"
    output += "|----------|------|------------------|--------|\n"
    
    overallocated = []
    underallocated = []
    
    for name, data in sorted(all_resources.items()):
        if data['total_allocation'] > 100:
            status = "🔴 Over-allocated"
            overallocated.append(name)
        elif data['total_allocation'] >= 80:
            status = "🟢 Optimal"
        elif data['total_allocation'] >= 50:
            status = "🟡 Under-utilized"
            underallocated.append(name)
        else:
            status = "⚪ Available"
            underallocated.append(name)
        output += f"| {name} | {data['role']} | {data['total_allocation']}% | {status} |\n"
    
    output += "\n### By Project\n\n"
    for key, project in projects.items():
        if not project:
            continue
        team = project.get("team", [])
        total_allocation = sum(m['allocation'] for m in team)
        output += f"**{project['project_name']}** - {len(team)} members, {total_allocation}% total capacity\n"
        for m in team:
            output += f"  - {m['name']} ({m['role']}): {m['allocation']}%\n"
        output += "\n"
    
    output += "### 💡 Recommendations\n\n"
    if overallocated:
        output += f"**Over-allocated Resources:** {', '.join(overallocated)}\n"
        output += "- Consider redistributing workload or hiring additional resources\n\n"
    if underallocated:
        output += f"**Under-utilized Resources:** {', '.join(underallocated)}\n"
        output += "- Consider assigning to blocked projects or new initiatives\n"
    return output


def get_milestone_status(project_key: Optional[str] = None) -> str:
    """Get detailed milestone tracking with predictions."""
    if project_key:
        projects = {project_key.upper(): get_project(project_key.upper())}
        if not projects[project_key.upper()]:
            return f"Project {project_key} not found."
    else:
        projects = ALL_PROJECTS
    
    output = "## 🎯 Milestone Guardian Report\n\n"
    today = datetime.now()
    at_risk_milestones = []
    upcoming_milestones = []
    
    for key, project in projects.items():
        if not project:
            continue
        output += f"### {project['project_name']}\n\n"
        milestones = project.get("milestones", [])
        output += "| Milestone | Due Date | Status | Progress | Days Left |\n"
        output += "|-----------|----------|--------|----------|----------|\n"
        
        for m in milestones:
            due = datetime.strptime(m['due_date'], "%Y-%m-%d")
            days_left = (due - today).days
            status_emoji = {"COMPLETED": "✅", "ON_TRACK": "🟢", "AT_RISK": "🟡", "NOT_STARTED": "⬜"}.get(m["status"], "❓")
            if days_left < 0:
                days_str = f"🔴 {abs(days_left)}d overdue"
            elif days_left <= 14:
                days_str = f"🟡 {days_left}d"
            else:
                days_str = f"{days_left}d"
            output += f"| {m['name']} | {m['due_date']} | {status_emoji} {m['status']} | {m['completion']}% | {days_str} |\n"
            if m['status'] in ['AT_RISK'] or (days_left < 14 and m['status'] != 'COMPLETED'):
                at_risk_milestones.append({'project': project['project_name'], 'milestone': m['name'], 'due': m['due_date'], 'days_left': days_left, 'completion': m['completion']})
            if days_left > 0 and days_left <= 30 and m['status'] != 'COMPLETED':
                upcoming_milestones.append({'project': project['project_name'], 'milestone': m['name'], 'due': m['due_date'], 'days_left': days_left})
        output += "\n"
    
    if at_risk_milestones:
        output += "### 🚨 At-Risk Milestones\n\n"
        for m in at_risk_milestones:
            output += f"- **{m['project']}**: {m['milestone']} - {m['days_left']}d left, {m['completion']}% complete\n"
        output += "\n"
    
    if upcoming_milestones:
        output += "### 📅 Upcoming Milestones (Next 30 Days)\n\n"
        for m in sorted(upcoming_milestones, key=lambda x: x['days_left']):
            output += f"- **{m['project']}**: {m['milestone']} - Due {m['due']} ({m['days_left']}d)\n"
    return output


def get_predictive_analytics(project_key: Optional[str] = None) -> str:
    """Generate predictive analytics with forecasting."""
    if project_key:
        projects = {project_key.upper(): get_project(project_key.upper())}
        if not projects[project_key.upper()]:
            return f"Project {project_key} not found."
    else:
        projects = ALL_PROJECTS
    
    output = "## 🔮 Predictive Analytics Report\n\n"
    output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    
    for key, project in projects.items():
        if not project:
            continue
        output += f"### {project['project_name']} ({key})\n\n"
        evm_data = project.get("evm", {})
        metrics = None
        if evm_data:
            metrics = calculate_evm(evm_data)
            output += "**Financial Forecast:**\n"
            output += f"- Current CPI: {metrics.CPI:.3f}\n"
            output += f"- Projected Final Cost (EAC): \${metrics.EAC:,.0f}\n"
            output += f"- Budget Variance (VAC): \${metrics.VAC:,.0f}\n"
            if metrics.VAC < 0:
                output += f"- 📉 **Projected Overrun:** \${abs(metrics.VAC):,.0f} ({abs(metrics.VAC)/metrics.BAC*100:.1f}%)\n"
            else:
                output += f"- 📈 **Projected Savings:** \${metrics.VAC:,.0f}\n"
            output += f"\n**Schedule Forecast:**\n"
            output += f"- Current SPI: {metrics.SPI:.3f}\n"
            if metrics.SPI < 1.0:
                delay_percent = (1 - metrics.SPI) * 100
                output += f"- 📉 **Projected Delay:** {delay_percent:.1f}% behind schedule\n"
                start = datetime.strptime(project['start_date'], "%Y-%m-%d")
                end = datetime.strptime(project['planned_end_date'], "%Y-%m-%d")
                total_weeks = (end - start).days / 7
                delay_weeks = total_weeks * (1 - metrics.SPI) / metrics.SPI
                output += f"- Estimated delay: {delay_weeks:.1f} weeks\n"
            else:
                output += f"- 📈 **Ahead of Schedule** by {(metrics.SPI - 1) * 100:.1f}%\n"
        
        sprints = project.get("sprints", [])
        velocities = [s['velocity'] for s in sprints if s['velocity']]
        if len(velocities) >= 3:
            output += f"\n**Velocity Trend:**\n"
            output += f"- History: {' → '.join(str(v) for v in velocities)}\n"
            if velocities[-1] < velocities[0]:
                decline_rate = (velocities[0] - velocities[-1]) / velocities[0] * 100
                output += f"- 📉 Declining by {decline_rate:.1f}%\n"
            else:
                increase_rate = (velocities[-1] - velocities[0]) / velocities[0] * 100
                output += f"- 📈 Improving by {increase_rate:.1f}%\n"
        
        risks = project.get("risks", [])
        blockers = project.get("blockers", [])
        high_risks = len([r for r in risks if r['probability'] == 'HIGH'])
        critical_blockers = len([b for b in blockers if b['impact'] == 'CRITICAL'])
        
        base_probability = 100
        if metrics and metrics.SPI < 0.9:
            base_probability -= 30
        elif metrics and metrics.SPI < 1.0:
            base_probability -= 15
        base_probability -= high_risks * 10
        base_probability -= critical_blockers * 15
        base_probability = max(5, min(95, base_probability))
        
        output += f"\n**On-Time Delivery Probability:** {base_probability}%\n"
        health = project['health']
        if health == 'RED':
            output += "- 🔴 **HIGH RISK** - Immediate intervention required\n"
        elif health == 'AMBER':
            output += "- 🟡 **MEDIUM RISK** - Close monitoring needed\n"
        else:
            output += "- 🟢 **LOW RISK** - On track\n"
        output += "\n---\n\n"
    return output


def get_workflow_status() -> str:
    """Analyze workflow efficiency and bottlenecks across projects."""
    output = "## ⚙️ Workflow Analysis\n\n"
    all_issues = []
    status_counts = {"Open": 0, "To Do": 0, "In Progress": 0, "Blocked": 0, "Done": 0}
    type_counts = {"Epic": 0, "Story": 0, "Task": 0, "Bug": 0}
    
    for key, project in ALL_PROJECTS.items():
        for issue in project.get("issues", []):
            issue_copy = issue.copy()
            issue_copy['project'] = key
            all_issues.append(issue_copy)
            status = issue.get('status', 'Unknown')
            if status in status_counts:
                status_counts[status] += 1
            itype = issue.get('type', 'Unknown')
            if itype in type_counts:
                type_counts[itype] += 1
    
    total_issues = len(all_issues)
    done_issues = status_counts.get('Done', 0)
    blocked_issues = status_counts.get('Blocked', 0)
    in_progress = status_counts.get('In Progress', 0)
    
    output += "### Workflow Health Metrics\n\n"
    output += f"- **Total Issues:** {total_issues}\n"
    output += f"- **Completed:** {done_issues} ({done_issues/total_issues*100:.1f}%)\n"
    output += f"- **In Progress:** {in_progress} ({in_progress/total_issues*100:.1f}%)\n"
    output += f"- **Blocked:** {blocked_issues} ({blocked_issues/total_issues*100:.1f}%)\n"
    
    output += f"\n### WIP Limits\n"
    output += f"- Current WIP: {in_progress} items\n"
    if in_progress > 10:
        output += f"- ⚠️ High WIP may indicate multitasking inefficiency\n"
    
    output += "\n### Bottleneck Analysis\n\n"
    all_blockers = get_all_blockers()
    if all_blockers:
        output += f"**Active Blockers:** {len(all_blockers)}\n"
        for b in all_blockers:
            blocked_date = datetime.strptime(b['blocked_since'], "%Y-%m-%d")
            days_blocked = (datetime.now() - blocked_date).days
            output += f"- [{b['project_key']}] {b['issue_key']}: {days_blocked}d blocked\n"
    else:
        output += "✅ No active blockers\n"
    
    output += "\n### Issue Type Distribution\n"
    for itype, count in type_counts.items():
        bar = "█" * int(count / total_issues * 20)
        output += f"- {itype}: {count} ({count/total_issues*100:.1f}%) {bar}\n"
    
    bug_count = type_counts.get('Bug', 0)
    bug_ratio = bug_count / total_issues * 100
    output += f"\n**Bug Ratio:** {bug_ratio:.1f}%"
    if bug_ratio > 20:
        output += " ⚠️ High - Consider quality improvements\n"
    else:
        output += " ✅ Healthy\n"
    return output


def get_ml_predictions(project_key: Optional[str] = None) -> str:
    """Get ML-powered predictions using Linear Regression and XGBoost."""
    try:
        from ml_models import (
            get_full_ml_prediction,
            get_feature_importance,
            EVMFeatureExtractor,
            ML_AVAILABLE,
            XGBOOST_AVAILABLE
        )
    except ImportError:
        return "⚠️ ML Models not available. Please ensure ml_models.py is in the project directory."
    
    if project_key:
        project = get_project(project_key.upper())
        if not project:
            return f"Project {project_key} not found."
        projects = {project_key.upper(): project}
    else:
        projects = ALL_PROJECTS
    
    output = "## 🤖 ML-Powered Predictive Analytics\n\n"
    output += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    output += f"*Models: Linear Regression, {'XGBoost' if XGBOOST_AVAILABLE else 'GradientBoosting'}*\n\n"
    
    for key, project in projects.items():
        predictions = get_full_ml_prediction(project)
        features = predictions['features']
        
        output += f"### 📊 {key}: {project['name']}\n\n"
        
        # EVM Features Used
        output += "#### 📈 Input Features (EVM Metrics)\n"
        output += f"| Metric | Value |\n|--------|-------|\n"
        output += f"| CPI | {features['cpi']:.2f} |\n"
        output += f"| SPI | {features['spi']:.2f} |\n"
        output += f"| % Complete | {features['percent_complete']:.1f}% |\n"
        output += f"| Risk Score | {features['risk_score']:.1f} |\n"
        output += f"| Active Blockers | {features['active_blockers']} |\n"
        output += f"| Velocity | {features['velocity']:.1f} |\n\n"
        
        # Cost Forecast
        cost = predictions['cost_forecast']
        output += "#### 💰 Cost Forecast (XGBoost)\n"
        output += f"- **Predicted Final Cost:** ${cost['predicted_cost']:,.0f}\n"
        output += f"- **Budget (BAC):** ${features['bac']:,.0f}\n"
        overrun_emoji = "🔴" if cost['cost_overrun_pct'] > 10 else ("🟡" if cost['cost_overrun_pct'] > 0 else "🟢")
        output += f"- **Cost Overrun:** {overrun_emoji} {cost['cost_overrun_pct']:.1f}%\n"
        output += f"- **Confidence:** {cost['confidence']:.0f}%\n"
        output += f"- **Range:** ${cost['lower_bound']:,.0f} - ${cost['upper_bound']:,.0f}\n\n"
        
        # Schedule Forecast
        schedule = predictions['schedule_forecast']
        output += "#### 📅 Schedule Forecast (Linear Regression)\n"
        status_emoji = "🟢" if schedule['status'] == 'ON_TRACK' else ("🟡" if schedule['status'] == 'AT_RISK' else "🔴")
        output += f"- **Status:** {status_emoji} {schedule['status']}\n"
        output += f"- **Predicted Delay:** {schedule['delay_days']:.0f} days\n"
        output += f"- **On-Time Probability:** {schedule['on_time_probability']:.0f}%\n"
        output += f"- **Confidence:** {schedule['confidence']:.0f}%\n\n"
        
        # Risk Classification
        risk = predictions['risk_classification']
        output += "#### ⚠️ Risk Classification (XGBoost)\n"
        risk_emoji = "🔴" if risk['risk_level'] == 'HIGH' else ("🟡" if risk['risk_level'] == 'MEDIUM' else "🟢")
        output += f"- **Risk Level:** {risk_emoji} {risk['risk_level']}\n"
        output += f"- **Confidence:** {risk['confidence']:.0f}%\n"
        output += f"- **Probabilities:** HIGH={risk['probabilities'].get('HIGH', 0)*100:.0f}%, "
        output += f"MEDIUM={risk['probabilities'].get('MEDIUM', 0)*100:.0f}%, "
        output += f"LOW={risk['probabilities'].get('LOW', 0)*100:.0f}%\n\n"
        
        # Resource Forecast
        resource = predictions['resource_forecast']
        output += "#### 👥 Resource Forecast (Linear Regression)\n"
        output += f"- **Current Team:** {resource['current_team']} FTEs\n"
        output += f"- **Recommended:** {resource['required_ftes']:.1f} FTEs\n"
        delta_emoji = "➕" if resource['delta'] > 0 else ("➖" if resource['delta'] < 0 else "✅")
        output += f"- **Delta:** {delta_emoji} {resource['delta']:+.1f}\n"
        output += f"- **Action:** {resource['recommendation']}\n\n"
        
        # Burn Rate
        burn = predictions['burn_rate_forecast']
        output += "#### 🔥 Burn Rate Forecast (XGBoost)\n"
        output += f"- **Predicted Monthly Burn:** ${burn['predicted_monthly_burn']:,.0f}\n"
        output += f"- **Budgeted Burn:** ${burn['budgeted_burn']:,.0f}\n"
        variance_emoji = "🔴" if burn['variance_pct'] > 10 else ("🟡" if burn['variance_pct'] > 0 else "🟢")
        output += f"- **Variance:** {variance_emoji} {burn['variance_pct']:+.1f}%\n"
        output += f"- **Runway:** {burn['runway_months']:.1f} months\n\n"
        
        output += "---\n\n"
    
    # Feature Importance
    output += "### 🎯 Feature Importance (Model Insights)\n\n"
    importance = get_feature_importance()
    output += "**Cost Model Drivers:**\n"
    for feat, imp in sorted(importance['cost_model'].items(), key=lambda x: x[1], reverse=True)[:4]:
        bar = "█" * int(imp * 20)
        output += f"- {feat}: {bar} {imp*100:.0f}%\n"
    output += "\n"
    
    output += "**Schedule Model Drivers:**\n"
    for feat, imp in sorted(importance['schedule_model'].items(), key=lambda x: x[1], reverse=True)[:4]:
        bar = "█" * int(imp * 20)
        output += f"- {feat}: {bar} {imp*100:.0f}%\n"
    
    return output


# Export all tools
TOOL_FUNCTIONS = {
    "get_portfolio_overview": get_portfolio_overview,
    "get_project_details": get_project_details,
    "get_project_blockers": get_project_blockers,
    "get_project_risks": get_project_risks,
    "calculate_project_evm": calculate_project_evm,
    "get_sprint_status": get_sprint_status,
    "get_issue_breakdown": get_issue_breakdown,
    "generate_escalation_report": generate_escalation_report,
    "get_schedule_analysis": get_schedule_analysis,
    "get_resource_allocation": get_resource_allocation,
    "get_milestone_status": get_milestone_status,
    "get_predictive_analytics": get_predictive_analytics,
    "get_workflow_status": get_workflow_status,
    "get_ml_predictions": get_ml_predictions,
}

if __name__ == "__main__":
    print(get_portfolio_overview())
