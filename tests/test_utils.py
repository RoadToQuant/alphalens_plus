import numpy as np
import pandas as pd
import pytest
from alphalens_plus import utils


def test_compute_forward_returns_open_to_open(mock_prices):
    result = utils.compute_forward_returns(
        mock_prices, periods=(1, 2), method='open-to-open'
    )
    assert '1D' in result.columns
    assert '2D' in result.columns
    assert result['1D'].notna().sum() > 0


def test_compute_forward_returns_close_to_close(mock_prices):
    result = utils.compute_forward_returns(
        mock_prices, periods=(1,), method='close-to-close'
    )
    assert '1D' in result.columns
    assert result['1D'].notna().sum() > 0


def test_get_clean_factor_and_forward_returns(mock_prices, mock_factor):
    result = utils.get_clean_factor_and_forward_returns(
        mock_factor, mock_prices, periods=(1,), method='open-to-open'
    )
    assert 'factor' in result.columns
    assert '1D' in result.columns
    assert result.index.names == ['date', 'order_book_id']


def test_quantize_factor(mock_factor):
    factor_data = mock_factor.copy()
    q = utils.quantize_factor(factor_data, quantiles=5)
    assert q.name == 'factor_quantile'
    assert set(q.dropna().unique()).issubset({1, 2, 3, 4, 5})


def test_rank_factor(mock_factor):
    factor_data = mock_factor.copy()
    r = utils.rank_factor(factor_data, ascending=False)
    assert r.name == 'factor_rank'
    for _, group in r.groupby(level='date'):
        assert sorted(group.values) == [1, 2, 3]
