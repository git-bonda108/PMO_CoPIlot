"""
PMO CoPilot - Earned Value Management (EVM) Calculator
Provides comprehensive EVM analysis with variance calculations and forecasting
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EVMMetrics:
    """Complete EVM metrics with all standard calculations"""
    # Core Values
    BAC: float  # Budget at Completion
    PV: float   # Planned Value
    EV: float   # Earned Value
    AC: float   # Actual Cost

    # Variance Metrics
    CV: float   # Cost Variance (EV - AC)
    SV: float   # Schedule Variance (EV - PV)

    # Performance Indices
    CPI: float  # Cost Performance Index (EV / AC)
    SPI: float  # Schedule Performance Index (EV / PV)

    # Forecasts
    EAC: float  # Estimate at Completion
    ETC: float  # Estimate to Complete
    VAC: float  # Variance at Completion
    TCPI: float # To-Complete Performance Index

    # Percent Complete
    percent_complete: float
    percent_spent: float

    # Health Assessment
    cost_health: str
    schedule_health: str
    overall_health: str

def calculate_evm(evm_data: Dict[str, float]) -> EVMMetrics:
    """
    Calculate comprehensive EVM metrics from raw data.

    Args:
        evm_data: Dictionary containing BAC, PV, EV, AC values

    Returns:
        EVMMetrics dataclass with all calculated values
    """
    BAC = evm_data.get("BAC", 0)
    PV = evm_data.get("PV", 0)
    EV = evm_data.get("EV", 0)
    AC = evm_data.get("AC", 0)

    # Variance Calculations
    CV = EV - AC  # Positive = under budget
    SV = EV - PV  # Positive = ahead of schedule

    # Performance Indices (avoid division by zero)
    CPI = EV / AC if AC > 0 else 0
    SPI = EV / PV if PV > 0 else 0

    # Forecasting
    # EAC using CPI method (most common)
    EAC = BAC / CPI if CPI > 0 else BAC * 2
    ETC = EAC - AC
    VAC = BAC - EAC

    # TCPI - efficiency needed to complete on budget
    remaining_work = BAC - EV
    remaining_budget = BAC - AC
    TCPI = remaining_work / remaining_budget if remaining_budget > 0 else float('inf')

    # Percent calculations
    percent_complete = (EV / BAC * 100) if BAC > 0 else 0
    percent_spent = (AC / BAC * 100) if BAC > 0 else 0

    # Health Assessment
    cost_health = _assess_cost_health(CPI)
    schedule_health = _assess_schedule_health(SPI)
    overall_health = _assess_overall_health(CPI, SPI)

    return EVMMetrics(
        BAC=BAC, PV=PV, EV=EV, AC=AC,
        CV=CV, SV=SV,
        CPI=round(CPI, 3), SPI=round(SPI, 3),
        EAC=round(EAC, 2), ETC=round(ETC, 2), VAC=round(VAC, 2),
        TCPI=round(TCPI, 3),
        percent_complete=round(percent_complete, 1),
        percent_spent=round(percent_spent, 1),
        cost_health=cost_health,
        schedule_health=schedule_health,
        overall_health=overall_health
    )

def _assess_cost_health(cpi: float) -> str:
    """Assess cost health based on CPI"""
    if cpi >= 1.0:
        return "GREEN"
    elif cpi >= 0.9:
        return "AMBER"
    else:
        return "RED"

def _assess_schedule_health(spi: float) -> str:
    """Assess schedule health based on SPI"""
    if spi >= 1.0:
        return "GREEN"
    elif spi >= 0.9:
        return "AMBER"
    else:
        return "RED"

def _assess_overall_health(cpi: float, spi: float) -> str:
    """Assess overall project health"""
    if cpi >= 1.0 and spi >= 1.0:
        return "GREEN"
    elif cpi >= 0.9 and spi >= 0.9:
        return "AMBER"
    else:
        return "RED"

def format_evm_report(metrics: EVMMetrics, project_name: str = "Project") -> str:
    """Format EVM metrics into a readable report"""

    currency = lambda x: f"${x:,.2f}"

    report = f"""
================================================================================
                    EARNED VALUE MANAGEMENT REPORT
                    {project_name}
                    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
================================================================================

CORE METRICS
------------
Budget at Completion (BAC):     {currency(metrics.BAC)}
Planned Value (PV):             {currency(metrics.PV)}
Earned Value (EV):              {currency(metrics.EV)}
Actual Cost (AC):               {currency(metrics.AC)}

VARIANCE ANALYSIS
-----------------
Cost Variance (CV):             {currency(metrics.CV)} {'(Under Budget)' if metrics.CV >= 0 else '(Over Budget)'}
Schedule Variance (SV):         {currency(metrics.SV)} {'(Ahead)' if metrics.SV >= 0 else '(Behind)'}

PERFORMANCE INDICES
-------------------
Cost Performance Index (CPI):   {metrics.CPI} {'(Efficient)' if metrics.CPI >= 1 else '(Inefficient)'}
Schedule Performance Index:     {metrics.SPI} {'(On/Ahead)' if metrics.SPI >= 1 else '(Behind)'}

FORECASTS
---------
Estimate at Completion (EAC):   {currency(metrics.EAC)}
Estimate to Complete (ETC):     {currency(metrics.ETC)}
Variance at Completion (VAC):   {currency(metrics.VAC)}
To-Complete Perf Index (TCPI):  {metrics.TCPI}

PROGRESS
--------
Work Complete:                  {metrics.percent_complete}%
Budget Spent:                   {metrics.percent_spent}%

HEALTH STATUS
-------------
Cost Health:                    {metrics.cost_health}
Schedule Health:                {metrics.schedule_health}
Overall Health:                 {metrics.overall_health}

================================================================================
"""
    return report

def get_evm_insights(metrics: EVMMetrics) -> Dict[str, Any]:
    """Generate AI-ready insights from EVM metrics"""

    insights = {
        "summary": "",
        "concerns": [],
        "recommendations": [],
        "forecast_accuracy": ""
    }

    # Summary
    if metrics.overall_health == "GREEN":
        insights["summary"] = "Project is performing well on both cost and schedule."
    elif metrics.overall_health == "AMBER":
        insights["summary"] = "Project has minor variances requiring attention."
    else:
        insights["summary"] = "Project has significant issues requiring immediate action."

    # Concerns
    if metrics.CPI < 1.0:
        overrun = (1 - metrics.CPI) * 100
        insights["concerns"].append(
            f"Cost overrun of {overrun:.1f}% - spending more than planned for work completed"
        )

    if metrics.SPI < 1.0:
        delay = (1 - metrics.SPI) * 100
        insights["concerns"].append(
            f"Schedule delay of {delay:.1f}% - less work completed than planned"
        )

    if metrics.TCPI > 1.1:
        insights["concerns"].append(
            f"TCPI of {metrics.TCPI} indicates very high efficiency needed to complete on budget"
        )

    # Recommendations
    if metrics.CPI < 0.9:
        insights["recommendations"].append("Conduct cost audit to identify waste")
        insights["recommendations"].append("Consider scope reduction or additional funding")

    if metrics.SPI < 0.9:
        insights["recommendations"].append("Add resources or reduce scope")
        insights["recommendations"].append("Review and remove blockers immediately")

    if metrics.EAC > metrics.BAC * 1.1:
        insights["recommendations"].append(
            f"Budget increase of ${metrics.EAC - metrics.BAC:,.0f} may be needed"
        )

    return insights

if __name__ == "__main__":
    # Test with sample data
    test_data = {
        "BAC": 2500000,
        "PV": 1875000,
        "EV": 1500000,
        "AC": 1875000,
    }

    metrics = calculate_evm(test_data)
    print(format_evm_report(metrics, "E-Commerce Platform Migration"))
    print("\nInsights:", get_evm_insights(metrics))
