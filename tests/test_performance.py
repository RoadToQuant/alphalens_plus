import numpy as np
import pandas as pd
import pytest
from alphalens_plus import performance as perf


def test_factor_weights(mock_factor_data):
    weights = perf.factor_weights(mock_factor_data)
    assert weights.name == 'weight'
    for _, group in weights.groupby(level='date'):
        assert np.isclose(group.abs().sum(), 1.0)


def test_factor_information_coefficient(mock_factor_data):
    ic = perf.factor_information_coefficient(mock_factor_data)
    assert isinstance(ic, pd.DataFrame)
    assert '1D' in ic.columns
    assert len(ic) == 5


def test_mean_information_coefficient(mock_factor_data):
    mic = perf.mean_information_coefficient(mock_factor_data)
    assert isinstance(mic, pd.Series)
    assert '1D' in mic.index
