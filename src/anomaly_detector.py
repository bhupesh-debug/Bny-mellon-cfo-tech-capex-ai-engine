"""
anomaly_detector.py
Machine Learning CapEx Overrun & Milestone Slippage Anomaly Detector
Author: Bhupesh Chandra Dimri (M.S. Accounting Analytics & Data Technology, Pace University)
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import Tuple


class CapExAnomalyDetector:
    """
    Unsupervised Isolation Forest to flag technology projects at elevated risk of
    budget overruns, burn-rate spikes, and milestone delivery delays before committee reviews.
    """

    def __init__(self, contamination: float = 0.08, random_state: int = 42):
        self.model = IsolationForest(contamination=contamination, random_state=random_state)
        self.features = ['burn_rate_ratio', 'milestone_delay_days', 'change_order_count', 'budget_consumed_pct']

    def fit_predict(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        
        # Ensure required features exist
        for f in self.features:
            if f not in data.columns:
                raise ValueError(f"Missing required feature '{f}' in project dataset.")

        X = data[self.features].fillna(0)
        
        # Isolation Forest prediction: -1 = Anomaly, 1 = Normal
        data['anomaly_label'] = self.model.fit_predict(X)
        data['anomaly_score'] = self.model.decision_function(X)
        
        data['risk_status'] = np.where(
            data['anomaly_label'] == -1,
            'CRITICAL_OVERRUN_ALERT',
            'ON_TRACK'
        )

        return data
