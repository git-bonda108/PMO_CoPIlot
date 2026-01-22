"""
PMO CoPilot - Mock JIRA Data Generator
Multiple project variations with realistic data for demo purposes
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

# ============================================
# PROJECT 1: E-Commerce Platform Migration
# Status: At Risk (Schedule Slippage)
# ============================================

ECOMMERCE_PROJECT = {
    "project_key": "ECOM",
    "project_name": "E-Commerce Platform Migration",
    "project_manager": "Sarah Chen",
    "start_date": "2025-09-01",
    "planned_end_date": "2026-03-31",
    "budget": 2500000,
    "spent": 1875000,
    "status": "AT_RISK",
    "health": "AMBER",
    "sprints": [
        {"id": 1, "name": "Sprint 1 - Foundation", "status": "COMPLETED", "velocity": 42},
        {"id": 2, "name": "Sprint 2 - User Auth", "status": "COMPLETED", "velocity": 38},
        {"id": 3, "name": "Sprint 3 - Product Catalog", "status": "COMPLETED", "velocity": 35},
        {"id": 4, "name": "Sprint 4 - Cart & Checkout", "status": "IN_PROGRESS", "velocity": 28},
        {"id": 5, "name": "Sprint 5 - Payment Integration", "status": "PLANNED", "velocity": None},
    ],
    "issues": [
        {"key": "ECOM-101", "type": "Epic", "summary": "User Authentication System", "status": "Done", "assignee": "Mike Johnson", "story_points": 21, "priority": "High"},
        {"key": "ECOM-102", "type": "Epic", "summary": "Product Catalog Management", "status": "Done", "assignee": "Lisa Wang", "story_points": 34, "priority": "High"},
        {"key": "ECOM-103", "type": "Epic", "summary": "Shopping Cart & Checkout", "status": "In Progress", "assignee": "Tom Brown", "story_points": 55, "priority": "Critical"},
        {"key": "ECOM-104", "type": "Epic", "summary": "Payment Gateway Integration", "status": "To Do", "assignee": "Anna Smith", "story_points": 34, "priority": "Critical"},
        {"key": "ECOM-201", "type": "Story", "summary": "Implement OAuth2 login", "status": "Done", "assignee": "Mike Johnson", "story_points": 8, "priority": "High"},
        {"key": "ECOM-202", "type": "Story", "summary": "Add product search functionality", "status": "Done", "assignee": "Lisa Wang", "story_points": 5, "priority": "Medium"},
        {"key": "ECOM-203", "type": "Story", "summary": "Shopping cart persistence", "status": "In Progress", "assignee": "Tom Brown", "story_points": 8, "priority": "High"},
        {"key": "ECOM-204", "type": "Bug", "summary": "Cart total calculation error", "status": "In Progress", "assignee": "Tom Brown", "story_points": 3, "priority": "Critical"},
        {"key": "ECOM-205", "type": "Story", "summary": "Stripe payment integration", "status": "To Do", "assignee": "Anna Smith", "story_points": 13, "priority": "Critical"},
        {"key": "ECOM-206", "type": "Bug", "summary": "Session timeout not working", "status": "Open", "assignee": "Mike Johnson", "story_points": 2, "priority": "High"},
        {"key": "ECOM-207", "type": "Story", "summary": "Order confirmation emails", "status": "To Do", "assignee": "Lisa Wang", "story_points": 5, "priority": "Medium"},
        {"key": "ECOM-208", "type": "Task", "summary": "Performance testing setup", "status": "To Do", "assignee": "DevOps Team", "story_points": 8, "priority": "High"},
    ],
    "blockers": [
        {"issue_key": "ECOM-204", "description": "Critical bug blocking checkout flow", "blocked_since": "2026-01-15", "impact": "HIGH"},
        {"issue_key": "ECOM-205", "description": "Waiting for Stripe API credentials from finance", "blocked_since": "2026-01-10", "impact": "CRITICAL"},
    ],
    "risks": [
        {"id": "R001", "description": "Payment integration delay may push launch date", "probability": "HIGH", "impact": "HIGH", "mitigation": "Parallel development of PayPal as backup"},
        {"id": "R002", "description": "Performance issues under load", "probability": "MEDIUM", "impact": "HIGH", "mitigation": "Early load testing scheduled"},
        {"id": "R003", "description": "Third-party API rate limits", "probability": "LOW", "impact": "MEDIUM", "mitigation": "Implement caching layer"},
    ],
    "team": [
        {"name": "Sarah Chen", "role": "Project Manager", "allocation": 100},
        {"name": "Mike Johnson", "role": "Senior Developer", "allocation": 100},
        {"name": "Lisa Wang", "role": "Full Stack Developer", "allocation": 100},
        {"name": "Tom Brown", "role": "Backend Developer", "allocation": 100},
        {"name": "Anna Smith", "role": "Payment Specialist", "allocation": 50},
    ],
    "milestones": [
        {"name": "Phase 1: Foundation", "due_date": "2025-11-30", "status": "COMPLETED", "completion": 100},
        {"name": "Phase 2: Core Features", "due_date": "2026-01-31", "status": "AT_RISK", "completion": 75},
        {"name": "Phase 3: Payment & Launch", "due_date": "2026-03-31", "status": "NOT_STARTED", "completion": 0},
    ],
    "evm": {
        "BAC": 2500000,
        "PV": 1875000,
        "EV": 1500000,
        "AC": 1875000,
    }
}

# ============================================
# PROJECT 2: Mobile App Development
# Status: On Track (Green)
# ============================================

MOBILE_APP_PROJECT = {
    "project_key": "MAPP",
    "project_name": "Customer Mobile App v2.0",
    "project_manager": "David Kim",
    "start_date": "2025-10-01",
    "planned_end_date": "2026-04-30",
    "budget": 1800000,
    "spent": 900000,
    "status": "ON_TRACK",
    "health": "GREEN",
    "sprints": [
        {"id": 1, "name": "Sprint 1 - App Architecture", "status": "COMPLETED", "velocity": 45},
        {"id": 2, "name": "Sprint 2 - Core UI", "status": "COMPLETED", "velocity": 48},
        {"id": 3, "name": "Sprint 3 - API Integration", "status": "IN_PROGRESS", "velocity": 44},
        {"id": 4, "name": "Sprint 4 - Offline Mode", "status": "PLANNED", "velocity": None},
    ],
    "issues": [
        {"key": "MAPP-101", "type": "Epic", "summary": "App Architecture & Setup", "status": "Done", "assignee": "James Lee", "story_points": 21, "priority": "High"},
        {"key": "MAPP-102", "type": "Epic", "summary": "Core UI Components", "status": "Done", "assignee": "Emily Davis", "story_points": 34, "priority": "High"},
        {"key": "MAPP-103", "type": "Epic", "summary": "Backend API Integration", "status": "In Progress", "assignee": "Chris Wilson", "story_points": 42, "priority": "High"},
        {"key": "MAPP-201", "type": "Story", "summary": "Implement React Native navigation", "status": "Done", "assignee": "James Lee", "story_points": 8, "priority": "High"},
        {"key": "MAPP-202", "type": "Story", "summary": "Design system implementation", "status": "Done", "assignee": "Emily Davis", "story_points": 13, "priority": "High"},
        {"key": "MAPP-203", "type": "Story", "summary": "REST API client setup", "status": "In Progress", "assignee": "Chris Wilson", "story_points": 8, "priority": "High"},
        {"key": "MAPP-204", "type": "Story", "summary": "Push notification service", "status": "In Progress", "assignee": "James Lee", "story_points": 5, "priority": "Medium"},
        {"key": "MAPP-205", "type": "Bug", "summary": "iOS keyboard overlap issue", "status": "Done", "assignee": "Emily Davis", "story_points": 2, "priority": "Medium"},
    ],
    "blockers": [],
    "risks": [
        {"id": "R001", "description": "App Store approval delays", "probability": "MEDIUM", "impact": "MEDIUM", "mitigation": "Early submission for review"},
        {"id": "R002", "description": "iOS/Android feature parity", "probability": "LOW", "impact": "LOW", "mitigation": "Shared codebase with React Native"},
    ],
    "team": [
        {"name": "David Kim", "role": "Project Manager", "allocation": 100},
        {"name": "James Lee", "role": "Mobile Lead", "allocation": 100},
        {"name": "Emily Davis", "role": "UI/UX Developer", "allocation": 100},
        {"name": "Chris Wilson", "role": "Backend Developer", "allocation": 75},
    ],
    "milestones": [
        {"name": "Alpha Release", "due_date": "2026-01-15", "status": "COMPLETED", "completion": 100},
        {"name": "Beta Release", "due_date": "2026-03-01", "status": "ON_TRACK", "completion": 45},
        {"name": "Production Launch", "due_date": "2026-04-30", "status": "NOT_STARTED", "completion": 0},
    ],
    "evm": {
        "BAC": 1800000,
        "PV": 900000,
        "EV": 945000,
        "AC": 900000,
    }
}

# ============================================
# PROJECT 3: Data Platform Modernization
# Status: Critical (Major Issues)
# ============================================

DATA_PLATFORM_PROJECT = {
    "project_key": "DPLAT",
    "project_name": "Data Platform Modernization",
    "project_manager": "Rachel Green",
    "start_date": "2025-07-01",
    "planned_end_date": "2026-06-30",
    "budget": 4500000,
    "spent": 3150000,
    "status": "CRITICAL",
    "health": "RED",
    "sprints": [
        {"id": 1, "name": "Sprint 1 - Assessment", "status": "COMPLETED", "velocity": 35},
        {"id": 2, "name": "Sprint 2 - Data Migration Design", "status": "COMPLETED", "velocity": 32},
        {"id": 3, "name": "Sprint 3 - ETL Pipeline", "status": "COMPLETED", "velocity": 28},
        {"id": 4, "name": "Sprint 4 - Data Warehouse", "status": "COMPLETED", "velocity": 25},
        {"id": 5, "name": "Sprint 5 - Analytics Layer", "status": "IN_PROGRESS", "velocity": 18},
        {"id": 6, "name": "Sprint 6 - ML Integration", "status": "BLOCKED", "velocity": None},
    ],
    "issues": [
        {"key": "DPLAT-101", "type": "Epic", "summary": "Legacy System Assessment", "status": "Done", "assignee": "Mark Taylor", "story_points": 21, "priority": "High"},
        {"key": "DPLAT-102", "type": "Epic", "summary": "Data Migration Framework", "status": "Done", "assignee": "Jennifer Wu", "story_points": 55, "priority": "Critical"},
        {"key": "DPLAT-103", "type": "Epic", "summary": "ETL Pipeline Development", "status": "Done", "assignee": "Robert Chen", "story_points": 89, "priority": "Critical"},
        {"key": "DPLAT-104", "type": "Epic", "summary": "Data Warehouse Implementation", "status": "In Progress", "assignee": "Mark Taylor", "story_points": 144, "priority": "Critical"},
        {"key": "DPLAT-105", "type": "Epic", "summary": "Analytics & Reporting Layer", "status": "In Progress", "assignee": "Jennifer Wu", "story_points": 89, "priority": "High"},
        {"key": "DPLAT-106", "type": "Epic", "summary": "ML Model Integration", "status": "Blocked", "assignee": "AI Team", "story_points": 55, "priority": "High"},
        {"key": "DPLAT-201", "type": "Bug", "summary": "Data corruption in ETL process", "status": "Open", "assignee": "Robert Chen", "story_points": 8, "priority": "Critical"},
        {"key": "DPLAT-202", "type": "Bug", "summary": "Memory leak in data pipeline", "status": "In Progress", "assignee": "Mark Taylor", "story_points": 5, "priority": "Critical"},
        {"key": "DPLAT-203", "type": "Story", "summary": "Implement data validation rules", "status": "In Progress", "assignee": "Jennifer Wu", "story_points": 13, "priority": "High"},
        {"key": "DPLAT-204", "type": "Task", "summary": "Production environment setup", "status": "Blocked", "assignee": "DevOps", "story_points": 8, "priority": "Critical"},
        {"key": "DPLAT-205", "type": "Bug", "summary": "Query performance degradation", "status": "Open", "assignee": "Robert Chen", "story_points": 5, "priority": "High"},
    ],
    "blockers": [
        {"issue_key": "DPLAT-201", "description": "Critical data corruption affecting 15% of migrated records", "blocked_since": "2026-01-05", "impact": "CRITICAL"},
        {"issue_key": "DPLAT-204", "description": "Cloud infrastructure approval pending from IT Security", "blocked_since": "2026-01-08", "impact": "CRITICAL"},
        {"issue_key": "DPLAT-106", "description": "ML team reassigned to priority project", "blocked_since": "2026-01-12", "impact": "HIGH"},
    ],
    "risks": [
        {"id": "R001", "description": "Data integrity issues may require full re-migration", "probability": "HIGH", "impact": "CRITICAL", "mitigation": "Implement comprehensive data validation"},
        {"id": "R002", "description": "Budget overrun likely due to scope creep", "probability": "HIGH", "impact": "HIGH", "mitigation": "Scope review with stakeholders"},
        {"id": "R003", "description": "Key resource attrition risk", "probability": "MEDIUM", "impact": "HIGH", "mitigation": "Knowledge transfer sessions"},
        {"id": "R004", "description": "Vendor dependency for cloud services", "probability": "MEDIUM", "impact": "MEDIUM", "mitigation": "Multi-cloud strategy"},
    ],
    "team": [
        {"name": "Rachel Green", "role": "Project Manager", "allocation": 100},
        {"name": "Mark Taylor", "role": "Data Architect", "allocation": 100},
        {"name": "Jennifer Wu", "role": "Senior Data Engineer", "allocation": 100},
        {"name": "Robert Chen", "role": "ETL Developer", "allocation": 100},
        {"name": "AI Team", "role": "ML Engineers", "allocation": 0},
    ],
    "milestones": [
        {"name": "Assessment Complete", "due_date": "2025-09-30", "status": "COMPLETED", "completion": 100},
        {"name": "Migration Framework Ready", "due_date": "2025-12-31", "status": "COMPLETED", "completion": 100},
        {"name": "Data Warehouse Live", "due_date": "2026-03-31", "status": "AT_RISK", "completion": 60},
        {"name": "Full Platform Launch", "due_date": "2026-06-30", "status": "AT_RISK", "completion": 25},
    ],
    "evm": {
        "BAC": 4500000,
        "PV": 3375000,
        "EV": 2700000,
        "AC": 3150000,
    }
}

# ============================================
# PROJECT 4: Security Compliance Initiative
# Status: On Track
# ============================================

SECURITY_PROJECT = {
    "project_key": "SECU",
    "project_name": "SOC2 Compliance Initiative",
    "project_manager": "Michael Ross",
    "start_date": "2025-11-01",
    "planned_end_date": "2026-05-31",
    "budget": 800000,
    "spent": 320000,
    "status": "ON_TRACK",
    "health": "GREEN",
    "sprints": [
        {"id": 1, "name": "Sprint 1 - Gap Analysis", "status": "COMPLETED", "velocity": 28},
        {"id": 2, "name": "Sprint 2 - Policy Development", "status": "COMPLETED", "velocity": 32},
        {"id": 3, "name": "Sprint 3 - Technical Controls", "status": "IN_PROGRESS", "velocity": 30},
    ],
    "issues": [
        {"key": "SECU-101", "type": "Epic", "summary": "SOC2 Gap Analysis", "status": "Done", "assignee": "Security Team", "story_points": 21, "priority": "High"},
        {"key": "SECU-102", "type": "Epic", "summary": "Policy & Procedure Documentation", "status": "Done", "assignee": "Compliance Team", "story_points": 34, "priority": "High"},
        {"key": "SECU-103", "type": "Epic", "summary": "Technical Security Controls", "status": "In Progress", "assignee": "DevSecOps", "story_points": 55, "priority": "Critical"},
        {"key": "SECU-201", "type": "Story", "summary": "Implement MFA across all systems", "status": "Done", "assignee": "IT Team", "story_points": 8, "priority": "Critical"},
        {"key": "SECU-202", "type": "Story", "summary": "Encryption at rest implementation", "status": "In Progress", "assignee": "DevSecOps", "story_points": 13, "priority": "Critical"},
        {"key": "SECU-203", "type": "Task", "summary": "Security awareness training", "status": "In Progress", "assignee": "HR", "story_points": 5, "priority": "Medium"},
    ],
    "blockers": [],
    "risks": [
        {"id": "R001", "description": "Audit timeline may shift", "probability": "LOW", "impact": "MEDIUM", "mitigation": "Regular auditor communication"},
    ],
    "team": [
        {"name": "Michael Ross", "role": "Project Manager", "allocation": 50},
        {"name": "Security Team", "role": "Security Engineers", "allocation": 100},
        {"name": "Compliance Team", "role": "Compliance Analysts", "allocation": 75},
    ],
    "milestones": [
        {"name": "Gap Analysis Complete", "due_date": "2025-12-15", "status": "COMPLETED", "completion": 100},
        {"name": "Policies Approved", "due_date": "2026-02-28", "status": "COMPLETED", "completion": 100},
        {"name": "Technical Controls Implemented", "due_date": "2026-04-30", "status": "ON_TRACK", "completion": 40},
        {"name": "SOC2 Audit Complete", "due_date": "2026-05-31", "status": "NOT_STARTED", "completion": 0},
    ],
    "evm": {
        "BAC": 800000,
        "PV": 320000,
        "EV": 336000,
        "AC": 320000,
    }
}

# ============================================
# ALL PROJECTS COLLECTION
# ============================================

ALL_PROJECTS = {
    "ECOM": ECOMMERCE_PROJECT,
    "MAPP": MOBILE_APP_PROJECT,
    "DPLAT": DATA_PLATFORM_PROJECT,
    "SECU": SECURITY_PROJECT,
}

def get_project(project_key: str) -> Dict[str, Any]:
    """Get a specific project by key"""
    return ALL_PROJECTS.get(project_key, {})

def get_all_projects() -> Dict[str, Dict[str, Any]]:
    """Get all projects"""
    return ALL_PROJECTS

def get_project_summary() -> List[Dict[str, Any]]:
    """Get summary of all projects for portfolio view"""
    summaries = []
    for key, project in ALL_PROJECTS.items():
        summaries.append({
            "project_key": key,
            "project_name": project["project_name"],
            "project_manager": project["project_manager"],
            "status": project["status"],
            "health": project["health"],
            "budget": project["budget"],
            "spent": project["spent"],
            "budget_utilization": round(project["spent"] / project["budget"] * 100, 1),
        })
    return summaries

def get_all_blockers() -> List[Dict[str, Any]]:
    """Get all blockers across all projects"""
    all_blockers = []
    for key, project in ALL_PROJECTS.items():
        for blocker in project.get("blockers", []):
            blocker_with_project = blocker.copy()
            blocker_with_project["project_key"] = key
            blocker_with_project["project_name"] = project["project_name"]
            all_blockers.append(blocker_with_project)
    return all_blockers

def get_all_risks() -> List[Dict[str, Any]]:
    """Get all risks across all projects"""
    all_risks = []
    for key, project in ALL_PROJECTS.items():
        for risk in project.get("risks", []):
            risk_with_project = risk.copy()
            risk_with_project["project_key"] = key
            risk_with_project["project_name"] = project["project_name"]
            all_risks.append(risk_with_project)
    return all_risks

if __name__ == "__main__":
    print("=== Project Portfolio Summary ===")
    for summary in get_project_summary():
        print(f"{summary['project_key']}: {summary['project_name']} - {summary['health']} ({summary['budget_utilization']}% budget used)")
