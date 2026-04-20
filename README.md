# AlphalensPlus: A better toolbox for factors' alpha analysis

基于 [Quantopian](https://github.com/quantopian) 的 [Alphalens](https://github.com/quantopian/alphalens) 开发的升级版因子分析工具箱，针对 A 股市场数据结构与交易规则做了适配与增强。

## 安装

```bash
# 使用 uv（推荐）
uv pip install -e ".[opt]"

# 或使用 pip
pip install -e ".[opt]"
```

> 若不需要组合优化（`opt` 模块），可省略 `[opt]`，无需安装 `cvxpy`。

## 快速开始

以下示例展示从**模拟数据**到**生成完整分析报告**的最小流程：

```python
import pandas as pd
import numpy as np
import alphalens_plus as ap

# 1. 构造模拟行情数据（长面板）
#    索引：(order_book_id, date)，必须包含 close 与 open 列
dates = pd.date_range('2023-01-01', periods=20, freq='B')
assets = ['000001.XSHE', '000002.XSHE', '000009.XSHE', '000012.XSHE']
np.random.seed(42)

prices = pd.DataFrame(
    {
        'close': 100 * np.exp(np.cumsum(np.random.randn(80) * 0.02 + 0.001)),
        'open' : 100 * np.exp(np.cumsum(np.random.randn(80) * 0.02 + 0.001)),
    },
    index=pd.MultiIndex.from_product(
        [assets, dates], names=['order_book_id', 'date']
    )
)

# 2. 构造模拟因子数据（长面板）
#    索引：(date, order_book_id)，列名为 factor
factor = pd.DataFrame(
    np.random.randn(80),
    index=pd.MultiIndex.from_product(
        [dates, assets], names=['date', 'order_book_id']
    ),
    columns=['factor']
)

# 3. 计算清洗后的因子与远期收益率
factor_data = ap.get_clean_factor_and_forward_returns(
    factor, prices, periods=(1, 5), method='open-to-open'
)

# 4. 生成完整 Tear Sheet 分析报告
ap.create_full_tear_sheet(factor_data)
```

### 核心 API 速览

`alphalens_plus` 已将最常用函数暴露在包顶层，可直接通过 `import alphalens_plus as ap` 调用：

| 功能 | 顶层 API |
|------|----------|
| 清洗因子 + 计算远期收益 | `ap.get_clean_factor_and_forward_returns` |
| 因子分位数分层 | `ap.quantize_factor` |
| 因子排序 | `ap.rank_factor` |
| 信息系数 IC | `ap.factor_information_coefficient` |
| 平均 IC | `ap.mean_information_coefficient` |
| 组合权重 | `ap.factor_weights` |
| 完整 Tear Sheet | `ap.create_full_tear_sheet` |
| 最小方差优化 | `ap.min_variance`（需安装 `cvxpy`） |

若需更细粒度的控制，仍可按需导入子模块：

```python
from alphalens_plus import utils, performance, plotting, tears
```

## 日志与更新记录

项目开发日志已迁移至 [LOGGING.md](LOGGING.md)。

## References

+ [quantopian/alphalens](https://github.com/quantopian/alphalens):
  + 原生alphalens项目，主体内容于2015年左右实现，目前可复用，但局部代码需更新。
  + 整体用作思路参考。

+ [stefan-jansen/alphalens-reloaded](https://github.com/stefan-jansen/alphalens-reloaded)
  + 大佬Stefan Jansen维护的alphalens项目，对最新版本python进行适配，可复用程度较高。
  + 是主要学习和参考的项目。

+ [github:vnpy_alphalens](https://github.com/vnpy/vnpy_alphalens)
  + vnpy的自适应版，更多面向回测系统使用，次要学习和参考项目。
