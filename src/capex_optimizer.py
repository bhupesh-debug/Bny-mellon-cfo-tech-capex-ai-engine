"""
capex_optimizer.py
Enterprise Tech CapEx Hurdle Rate Engine & Software Capitalization Model (ASC 350-40)
Author: Bhupesh Chandra Dimri (M.S. Accounting Analytics & Data Technology, Pace University)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any


class TechCapExModeler:
    """
    Evaluates technology capital outlays, software capitalization schedules (ASC 350-40),
    and project economics (NPV, IRR, Payback Period, and Operating Cost Efficiency).
    """

    def __init__(self, hurdle_rate: float = 0.095):
        """
        :param hurdle_rate: Minimum acceptable rate of return (BNY Enterprise WACC + Risk Premium).
        """
        self.hurdle_rate = hurdle_rate

    def evaluate_project_roi(
        self,
        project_name: str,
        initial_outlay: float,
        annual_cost_savings: List[float],
        useful_life_years: int = 5,
        capitalized_ratio: float = 0.75,
    ) -> Dict[str, Any]:
        """
        Computes capital metrics, capitalization breakdown, and investment approval recommendation.
        """
        cash_flows = [-abs(initial_outlay)] + list(annual_cost_savings[:useful_life_years])
        
        # Calculate NPV
        npv = sum(cf / ((1 + self.hurdle_rate) ** idx) for idx, cf in enumerate(cash_flows))
        
        # Calculate IRR
        irr = self._calculate_irr(cash_flows)
        
        # Payback period
        cumulative = np.cumsum(cash_flows)
        payback = useful_life_years
        for i, val in enumerate(cumulative):
            if val >= 0:
                payback = i
                break
                
        # Software Capitalization (ASC 350-40)
        capitalized_capex = initial_outlay * capitalized_ratio
        expensed_opex = initial_outlay * (1.0 - capitalized_ratio)
        annual_amortization = capitalized_capex / useful_life_years if useful_life_years > 0 else 0.0

        decision = "APPROVE" if npv > 0 and irr >= self.hurdle_rate else "REJECT"

        return {
            "project_name": project_name,
            "initial_outlay": round(initial_outlay, 2),
            "capitalized_capex": round(capitalized_capex, 2),
            "expensed_opex": round(expensed_opex, 2),
            "annual_amortization": round(annual_amortization, 2),
            "npv": round(npv, 2),
            "irr_percent": round(irr * 100, 2),
            "payback_years": payback,
            "hurdle_rate_percent": round(self.hurdle_rate * 100, 2),
            "decision": decision,
        }

    @staticmethod
    def _calculate_irr(cash_flows: List[float]) -> float:
        """Robust Newton-Raphson IRR solver with fallback."""
        r = 0.10
        for _ in range(100):
            npv = sum(cf / ((1 + r) ** i) for i, cf in enumerate(cash_flows))
            d_npv = sum(-i * cf / ((1 + r) ** (i + 1)) for i, cf in enumerate(cash_flows))
            if abs(d_npv) < 1e-7:
                break
            r_new = r - npv / d_npv
            if abs(r_new - r) < 1e-6:
                return r_new
            r = r_new
        return r
