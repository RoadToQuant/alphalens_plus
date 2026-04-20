import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def mock_prices():
    """构造模拟价格数据（长面板，索引为 order_book_id, date）"""
    dates = pd.date_range('2023-01-01', periods=5, freq='B')
    assets = ['A', 'B', 'C']
    np.random.seed(42)
    prices = pd.DataFrame(
        {
            'close': np.round(np.random.rand(15) * 10 + 100, 2),
            'open': np.round(np.random.rand(15) * 10 + 100, 2),
        },
        index=pd.MultiIndex.from_product(
            [assets, dates], names=['order_book_id', 'date']
        )
    )
    return prices


@pytest.fixture
def mock_factor(mock_prices):
    """构造模拟因子数据（索引为 date, order_book_id）"""
    index = mock_prices.index.swaplevel()
    factor = pd.DataFrame(
        np.random.randn(len(index)),
        index=index,
        columns=['factor']
    )
    return factor


@pytest.fixture
def mock_factor_data():
    """构造可直接用于 performance 模块的 factor_data（含 forward returns）"""
    dates = pd.date_range('2023-01-01', periods=5, freq='B')
    assets = ['A', 'B', 'C']
    np.random.seed(42)
    index = pd.MultiIndex.from_product(
        [dates, assets], names=['date', 'order_book_id']
    )
    factor_data = pd.DataFrame(
        {
            'factor': np.random.randn(15),
            '1D': np.random.randn(15) * 0.02,
            '2D': np.random.randn(15) * 0.03,
        },
        index=index
    )
    return factor_data
