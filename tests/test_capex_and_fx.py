"""
test_capex_and_fx.py
Comprehensive pytest test suite for BNY Mellon CFO Engine
Author: Bhupesh Chandra Dimri
"""

import pytest
import pandas as pd
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.capex_optimizer import TechCapExModeler
from src.fx_decomposer import FXVarianceDecomposer
from src.anomaly_detector import CapExAnomalyDetector
from src.data_generator import generate_synthetic_cfo_dataset


def test_tech_capex_approval():
    modeler = TechCapExModeler(hurdle_rate=0.095)
    res = modeler.evaluate_project_roi(
        project_name="Test Cloud Project",
        initial_outlay=10000000.0,
        annual_cost_savings=[3500000, 3500000, 3500000, 3500000],
        useful_life_years=4,
        capitalized_ratio=0.80
    )
    assert res["decision"] == "APPROVE"
    assert res["npv"] > 0
    assert res["capitalized_capex"] == 8000000.0
    assert res["expensed_opex"] == 2000000.0
    assert res["annual_amortization"] == 2000000.0


def test_tech_capex_rejection():
    modeler = TechCapExModeler(hurdle_rate=0.15)
    res = modeler.evaluate_project_roi(
        project_name="Low Return Project",
        initial_outlay=10000000.0,
        annual_cost_savings=[500000, 500000, 500000],
        useful_life_years=3
    )
    assert res["decision"] == "REJECT"
    assert res["npv"] < 0


def test_fx_variance_mathematical_identity():
    df_entities, _ = generate_synthetic_cfo_dataset()
    decomposed = FXVarianceDecomposer.decompose(df_entities)
    
    # Check each row satisfies: Total Variance USD == Operational Variance USD + FX Translation USD
    for _, row in decomposed.iterrows():
        expected_total = row['operational_variance_usd'] + row['fx_translation_usd']
        assert pytest.approx(row['total_variance_usd'], rel=1e-3) == expected_total


def test_executive_bridge_summary():
    df_entities, _ = generate_synthetic_cfo_dataset()
    decomposed = FXVarianceDecomposer.decompose(df_entities)
    bridge = FXVarianceDecomposer.summarize_executive_bridge(decomposed)
    
    expected_sum = bridge['operational_variance_usd'] + bridge['fx_translation_usd']
    assert pytest.approx(bridge['total_variance_usd'], rel=1e-3) == expected_sum


def test_anomaly_detection_execution():
    _, df_projects = generate_synthetic_cfo_dataset()
    detector = CapExAnomalyDetector(contamination=0.20)
    analyzed = detector.fit_predict(df_projects)
    
    assert 'risk_status' in analyzed.columns
    assert 'anomaly_score' in analyzed.columns
    assert set(analyzed['risk_status'].unique()).issubset({'CRITICAL_OVERRUN_ALERT', 'ON_TRACK'})
