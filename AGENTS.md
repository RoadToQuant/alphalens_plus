# AlphalensPlus Agent Guide

> 本文档面向 AI Coding Agent。阅读本文档前，假设你对本项目一无所知。

## 项目概述

**AlphalensPlus** 是一个面向量化投资的因子（Alpha）分析工具箱，基于 [Quantopian/Alphalens](https://github.com/quantopian/alphalens) 二次开发，针对 A 股市场数据结构与交易规则做了适配与增强。

- **包名**: `alphalens_plus`
- **当前版本**: `1.0.2`（硬编码于 `alphalens_plus/__init__.py`）
- **Python 版本要求**: `>=3.9.12`
- **作者**: msliu98 (`mingshuoliu98@163.com`)
- **许可证**: MIT License
- **README**: `README.md`（中文）

核心能力包括：
- 计算因子远期收益率（forward returns），支持 `open-to-open`、`close-to-close`、`open-to-close`、`vwap-to-vwap` 等多种方式；
- 因子分层（quantile）与排序（rank）；
- 信息系数（IC）与分组收益分析；
- 组合换手率（turnover）与权重计算；
- 集成 Matplotlib/Seaborn 的 Tear Sheet 可视化报表；
- 基于 CVXPY 的最小方差组合优化（`opt.py`）。

## 技术栈与运行时架构

- **语言**: Python 3.9+
- **核心依赖**（版本已锁定，升级需格外谨慎）：
  - `pandas==1.3.5`
  - `numpy==1.21.6`
  - `scipy`
  - `statsmodels`
  - `matplotlib`
  - `seaborn`
  - `loguru`
  - `six`
- **可选依赖**:
  - `cvxpy`（仅用于 `opt.py` 中的组合优化，要求 Python>=3.9；在 `pyproject.toml` 的 `[project.optional-dependencies]` 中声明为 `opt`）
- **内部/本地依赖**（非 pip 安装，只在特定测试/研究脚本中使用）：
  - `jtdata`：本地行情数据接口，用于获取业绩基准收益率等；
  - `jtalpha`、`mytools`：本地因子研究与回测工具链，仅在 `tests/main_opt_hperiod.py` 和 `tests/only_long_strat.py` 中引用。

**数据约定**:
- 使用 Pandas `DataFrame`，索引通常为两级 `MultiIndex`：第一级 `date`，第二级 `order_book_id`（A 股标的代码）。
- 价格数据为长面板格式，必须至少包含 `close` 和 `open` 列（因为默认采用 `open-to-open` 计算远期收益率）。
- 默认业绩基准为中证 500：`000905.XSHG`。

## 目录与模块划分

```
alphalens_plus/
├── __init__.py      # 版本号与模块导出
├── utils.py         # 核心工具：远期收益率计算、因子清洗、分层分箱、排序、基准收益率获取
├── performance.py   # 绩效指标：组合权重、换手率（quantile / rank / portfolio）、IC / Mean IC
├── plotting.py      # 可视化函数：IC 时间序列、分组收益柱状图、小提琴图、累计收益、热力图等
├── tears.py         # Tear Sheet 组装层：将 plotting + performance 组装为完整分析报告
├── opt.py           # 组合优化：最小方差、全局最小方差（GMV）权重求解
└── _logging.py      # loguru 日志配置（内部模块，避免与标准库 logging 冲突）

tests/
├── conftest.py             # pytest 公共 fixtures（模拟数据）
├── test_import.py          # 包导入与顶层 API 检查
├── test_utils.py           # utils 核心函数测试（模拟数据）
├── test_performance.py     # performance 核心函数测试（模拟数据）
├── test_opt.py             # opt 模块测试（可选依赖 cvxpy，未安装时自动跳过）
├── test_version.py         # 版本号格式断言
├── main_opt_hperiod.py     # 最优持仓周期研究脚本（非单元测试）
└── only_long_strat.py      # 纯多头策略回测研究脚本（非单元测试）

根目录配置:
├── pyproject.toml         # 项目配置与依赖（setuptools + PEP 621）
├── requirements.txt       # 依赖列表（保留参考，阿里云 PyPI 镜像）
├── .github/workflows/release.yml  # GitHub Actions：打标签时自动构建 wheel 并发布 Release
└── CLAUDE.md              # 通用 LLM 编码行为准则（与本文件互补）
```

## 构建与安装命令

本项目使用 `setuptools` + `pyproject.toml` 管理，兼容 `uv` / `pip` 等工具。

```bash
# 使用 uv 安装依赖（推荐）
uv pip install -e ".[opt]"

# 或使用 pip
pip install -e ".[opt]"

# 构建 wheel
python -m build --wheel
```

## 测试说明

测试框架使用 `pytest`，全部基于模拟数据，不依赖外部私有库或本地文件。

```bash
# 运行所有测试
pytest tests -v

# 或单独运行某个测试模块
pytest tests/test_utils.py -v
```

**重要限制**：
- `test_opt.py` 依赖可选包 `cvxpy`；若未安装，该模块会被自动跳过。
- `main_opt_hperiod.py` 和 `only_long_strat.py` 不是单元测试，而是研究脚本，内含大量硬编码的本地数据路径和外部包引用，**不要在 CI 中执行**。

## 代码风格与开发约定

- **语言**: 代码注释与新增文档字符串以**中文**为主；保留的原始 Alphalens 英文文档字符串未做全面替换。
- **命名**: 遵循原始 Alphalens 风格，函数名使用下划线命名法（`snake_case`），Pandas 操作密集。
- **索引约定**:
  - `utils.py` 中的 `compute_forward_returns` 返回的索引顺序为 `(asset_field, time_field)`；
  - `get_clean_factor_and_forward_returns` 会将其交换为 `(time_field, asset_field)` 以与 `factor` 数据合并；
  - 其余模块默认使用 `(date, order_book_id)` 的顺序。
- **常见标记**：代码中留有 `FIXME`、`TODO`、`FIXMEd` 等标记，表示已知的历史遗留问题或待优化点。修改相关逻辑前建议先搜索这些关键字。
- **版本管理**：版本号在 `pyproject.toml` 的 `project.version` 与 `alphalens_plus/__init__.py` 的 `__version__` 中同步硬编码。发布时需同时更新两处。
- **包级 API**：`__init__.py` 已将最常用函数直接暴露到 `alphalens_plus` 顶层命名空间，推荐直接 `from alphalens_plus import get_clean_factor_and_forward_returns, create_full_tear_sheet`。

## 发布流程

- 发布通过 GitHub Actions 自动化完成（`.github/workflows/release.yml`）。
- 推送以 `v` 开头的 tag（例如 `v1.0.3`）时，Action 会自动：
  1. 使用 Python 3.9 环境；
  2. 执行 `python -m build --wheel`；
  3. 将构建好的 `.whl` 上传为 GitHub Release 附件。
- 当前未配置自动上传 PyPI 的流程。

## 安全与注意事项

- **依赖版本锁定**：`pandas==1.3.5` 与 `numpy==1.21.6` 属于较旧版本。进行代码重构或升级依赖时，需重点验证 Pandas API 兼容性（尤其是 `MultiIndex`、`groupby`、`apply` 的行为差异）。
- **数据安全**：多个测试与研究脚本包含本地绝对路径（如 `E:\daily_mission\...`、`D:\msliu\...`）。切勿将这些路径提交到版本库，也不要在公共 CI 中运行这些脚本。
- **外部数据接口**：`utils.py` 中的 `get_benchmark_returns` 默认调用本地 `jtdata` 库。若该接口不存在，函数会抛出 `ModuleNotFoundError`。在生产环境中使用前应确保该依赖可用，或自行替换为其他行情数据源。
