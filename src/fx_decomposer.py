"""
fx_decomposer.py
Multi-Currency Foreign Exchange Variance Decomposition Engine
Author: Bhupesh Chandra Dimri (M.S. Accounting Analytics & Data Technology, Pace University)
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


class FXVarianceDecomposer:
    """
    Decomposes enterprise financial variance between actual and budgeted spend
    into Constant Currency Operational Variance and FX Translation Impact.
    """

    @staticmethod
    def decompose(df: pd.DataFrame) -> pd.DataFrame:
        """
        Input DataFrame schema:
        ['entity', 'currency', 'actual_local', 'budget_local', 'actual_fx_rate', 'budget_fx_rate']
        Note: FX rate is expressed as USD per 1 unit of Local Currency.
        """
        data = df.copy()

        # 1. Total Spend in USD
        data['actual_usd'] = data['actual_local'] * data['actual_fx_rate']
        data['budget_usd'] = data['budget_local'] * data['budget_fx_rate']
        data['total_variance_usd'] = data['actual_usd'] - data['budget_usd']

        # 2. Constant Currency Operational Variance:
        # Evaluates controllable business unit execution at budgeted foreign exchange rate
        data['operational_variance_usd'] = (data['actual_local'] - data['budget_local']) * data['budget_fx_rate']

        # 3. FX Translation Impact:
        # Isolates macroeconomic currency swings applied to actual local spend
        data['fx_translation_usd'] = data['actual_local'] * (data['actual_fx_rate'] - data['budget_fx_rate'])

        # 4. Mathematical Identity Check:
        # Total Variance USD == Operational Variance USD + FX Translation USD
        reconciled = data['operational_variance_usd'] + data['fx_translation_usd']
        discrepancy = np.abs(data['total_variance_usd'] - reconciled)
        assert np.all(discrepancy < 1e-2), f"Reconciliation error detected: {discrepancy.max()}"

        # 5. Percent attribution
        data['operational_share_pct'] = np.where(
            data['total_variance_usd'] != 0,
            (data['operational_variance_usd'] / data['total_variance_usd']) * 100,
            0.0
        )
        data['fx_share_pct'] = np.where(
            data['total_variance_usd'] != 0,
            (data['fx_translation_usd'] / data['total_variance_usd']) * 100,
            0.0
        )

        return data

    @staticmethod
    def summarize_executive_bridge(decomposed_df: pd.DataFrame) -> Dict[str, float]:
        """Returns consolidated enterprise bridge numbers for CFO deck."""
        total_actual = float(decomposed_df['actual_usd'].sum())
        total_budget = float(decomposed_df['budget_usd'].sum())
        total_variance = float(decomposed_df['total_variance_usd'].sum())
        operational_var = float(decomposed_df['operational_variance_usd'].sum())
        fx_var = float(decomposed_df['fx_translation_usd'].sum())

        return {
            "total_budget_usd": round(total_budget, 2),
            "total_actual_usd": round(total_actual, 2),
            "total_variance_usd": round(total_variance, 2),
            "operational_variance_usd": round(operational_var, 2),
            "fx_translation_usd": round(fx_var, 2),
        }
