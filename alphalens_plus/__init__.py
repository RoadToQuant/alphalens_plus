__version__ = '1.0.3'

# 将最常用的 API 直接暴露在包顶层，简化外部调用
from .utils import (
    compute_forward_returns,
    get_clean_factor_and_forward_returns,
    quantize_factor,
    rank_factor,
    get_benchmark_returns,
)
from .performance import (
    factor_information_coefficient,
    mean_information_coefficient,
    factor_weights,
    quantile_turnover,
)
from .tears import (
    create_full_tear_sheet,
    create_summary_tear_sheet,
    create_returns_tear_sheet,
    create_information_tear_sheet,
    create_turnover_tear_sheet,
)
_opt_available = False
try:
    from .opt import (
        min_variance,
        calculate_gmv_weights_with_cvxpy,
        cal_variance,
    )
    _opt_available = True
except ImportError:
    pass

__all__ = [
    '__version__',
    # utils
    'compute_forward_returns',
    'get_clean_factor_and_forward_returns',
    'quantize_factor',
    'rank_factor',
    'get_benchmark_returns',
    # performance
    'factor_information_coefficient',
    'mean_information_coefficient',
    'factor_weights',
    'quantile_turnover',
    # tears
    'create_full_tear_sheet',
    'create_summary_tear_sheet',
    'create_returns_tear_sheet',
    'create_information_tear_sheet',
    'create_turnover_tear_sheet',
    # 子模块保留，方便按需深度使用
    'utils',
    'performance',
    'plotting',
    'tears',
    'opt',
]

if _opt_available:
    __all__.extend([
        'min_variance',
        'calculate_gmv_weights_with_cvxpy',
        'cal_variance',
    ])
