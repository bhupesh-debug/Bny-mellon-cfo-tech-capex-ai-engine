"""
data_generator.py
Generates realistic enterprise Tech CapEx and multi-currency subsidiary datasets for BNY Mellon.
Author: Bhupesh Chandra Dimri
"""

import numpy as np
import pandas as pd
from typing import Tuple


def generate_synthetic_cfo_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
    1. Multi-Currency Global Entities DataFrame (for FX Variance Decomposition)
    2. Enterprise Technology CapEx Projects DataFrame (for Hurdle Rate & Anomaly Detection)
    """
    # 1. Multi-Currency Global Entities
    entities = [
        {"entity": "BNY London Branch (UK Custody)", "currency": "GBP", "actual_local": 48500000.0, "budget_local": 45000000.0, "actual_fx_rate": 1.2850, "budget_fx_rate": 1.2400},
        {"entity": "BNY European Bank SE (Frankfurt)", "currency": "EUR", "actual_local": 72000000.0, "budget_local": 75000000.0, "actual_fx_rate": 1.0820, "budget_fx_rate": 1.1000},
        {"entity": "BNY Tokyo Branch (Japan Securities)", "currency": "JPY", "actual_local": 6200000000.0, "budget_local": 5800000000.0, "actual_fx_rate": 0.00645, "budget_fx_rate": 0.00710},
        {"entity": "BNY Singapore Sub (APAC Wealth Services)", "currency": "SGD", "actual_local": 34000000.0, "budget_local": 32500000.0, "actual_fx_rate": 0.7550, "budget_fx_rate": 0.7400},
        {"entity": "BNY Sydney Branch (Australia Clearing)", "currency": "AUD", "actual_local": 29000000.0, "budget_local": 28000000.0, "actual_fx_rate": 0.6520, "budget_fx_rate": 0.6700},
        {"entity": "BNY Zurich Office (Swiss Private Custody)", "currency": "CHF", "actual_local": 18500000.0, "budget_local": 18000000.0, "actual_fx_rate": 1.1350, "budget_fx_rate": 1.1100},
    ]
    df_entities = pd.DataFrame(entities)

    # 2. Enterprise Tech CapEx Projects
    projects = [
        {"project_id": "PRJ-CLOUD-01", "project_name": "Core Custody AWS Cloud Modernization", "initial_budget": 25000000, "actual_spend": 26200000, "burn_rate_ratio": 1.08, "milestone_delay_days": 12, "change_order_count": 3, "budget_consumed_pct": 104.8},
        {"project_id": "PRJ-AI-02", "project_name": "GenAI Corporate Action Extraction Engine", "initial_budget": 8500000, "actual_spend": 7900000, "burn_rate_ratio": 0.93, "milestone_delay_days": 0, "change_order_count": 1, "budget_consumed_pct": 92.9},
        {"project_id": "PRJ-CYBER-03", "project_name": "Zero-Trust Enterprise Identity & Access Mesh", "initial_budget": 14000000, "actual_spend": 18900000, "burn_rate_ratio": 1.45, "milestone_delay_days": 65, "change_order_count": 9, "budget_consumed_pct": 135.0},
        {"project_id": "PRJ-TREAS-04", "project_name": "Real-Time Collateral Management Platform", "initial_budget": 12000000, "actual_spend": 11800000, "burn_rate_ratio": 0.98, "milestone_delay_days": 4, "change_order_count": 2, "budget_consumed_pct": 98.3},
        {"project_id": "PRJ-ERP-05", "project_name": "Oracle Cloud Financials Modernization", "initial_budget": 32000000, "actual_spend": 39500000, "burn_rate_ratio": 1.38, "milestone_delay_days": 54, "change_order_count": 8, "budget_consumed_pct": 123.4},
        {"project_id": "PRJ-DATA-06", "project_name": "Enterprise Snowflake Data Lakehouse Tier 1", "initial_budget": 16000000, "actual_spend": 15400000, "burn_rate_ratio": 0.96, "milestone_delay_days": 0, "change_order_count": 2, "budget_consumed_pct": 96.2},
    ]
    df_projects = pd.DataFrame(projects)

    return df_entities, df_projects


if __name__ == "__main__":
    e, p = generate_synthetic_cfo_dataset()
    print("Entities:\n", e)
    print("\nProjects:\n", p)
