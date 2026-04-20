# 开发日志 / Logging

+ 20241223:
  + alphalens_plus中的plotting主要包含针对量化投资的集成度较高的绘图工具，可以结合[mplfinance]这个模组进行更新和加强，
    而这也是放在alphalens_plus的原因，因为alphalens_plus的导出结果一般都是returns和weights等，
    同时需要与行情数据结合查看，所以放在一起（同时还绑定empyrical）。
  + 而其他类似dash、plotly、bokech则由于更偏向可视化，所以是单独模组负责，更多是属于alphalens的下游模组（接收alphalens的输出）。
