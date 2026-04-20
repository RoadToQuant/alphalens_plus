import pytest

# cvxpy 是可选依赖，未安装时跳过本模块全部测试
cvxpy = pytest.importorskip("cvxpy")

import numpy as np
import pandas as pd
from alphalens_plus import opt


def test_min_variance():
    np.random.seed(42)
    returns = np.random.randn(100, 3) * 0.02 + 0.001
    prices = pd.DataFrame(
        100 * np.exp(np.cumsum(returns, axis=0)),
        columns=['A', 'B', 'C']
    )
    weights = opt.min_variance(prices)
    assert np.isclose(weights.sum(), 1.0)
    w_min = 1 / (len(weights) ** 1.5)
    assert all(weights >= w_min - 1e-6)
    assert all(weights <= 0.6 + 1e-6)
