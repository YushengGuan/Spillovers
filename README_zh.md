# 中国对全球光伏与风电成本贡献：修订稿复现包

本包对应2026年9月18日的最终分析口径，包含最新数据、计算代码、绘图代码、结果文件及英文说明。旧仓库的累计节约额和旧版情景不再作为本版结果。

## 使用方法

在解压后的仓库根目录，使用Python 3.10或以上版本：

```bash
python -m pip install -r requirements-tested.txt
python run_pipeline.py
```

默认流程会重新运行回归与诊断、成本分解、补充比较、CGE结果处理及绘图。**CGE部分默认读取包内已求解的最终均衡结果，不重新调用求解器**，因此默认复现不需要Julia和PATH许可证。完整重算CGE的方法见英文README。

`python verify.py`检查主要数值及一致性；首次解压可用`python verify.py --integrity`核验文件哈希。重跑会覆盖包内相应输出，因此哈希核验应在重跑之前进行。

## 核心口径

* 历史分析覆盖2010—2024年、10个光伏市场和13个风电市场。2024年中国相关净降本贡献分别为1,313.3085和378.5993美元/kW，均以2024年不变美元表示。
* 正文P、S、T、K、E分别对应代码中的`P_direct`、`S_share`、`T_cn_tariff`、`K_spillover`、`G_other`。`G_other`是沿用的字段名，代表E，不是专利知识存量G。
* S1与正文历史分解采用同一套年度拟合成本曲线；S2的碳价增量为60.8938931660美元/tCO₂，自2017年起保持至2050年。
* CGE的GW指标是发电量按固定容量因子换算的容量当量；不是独立模拟的装机存量。
* 包内是可复现的整理后数据及估计样本，不包含所有原始第三方报告全文。数据来源、手工转录、拼接和代理假设见`docs/DATA_SOURCES.md`及`data/price_provenance/`。

## 文件入口

| 要查看的内容 | 位置 |
|---|---|
| 主要运行说明与结果 | `README.md` |
| 正文与SI对应哪些文件 | `docs/MANUSCRIPT_MAP.md` |
| 数据来源和字段解释 | `docs/DATA_SOURCES.md`、`docs/DATA_DICTIONARY.md` |
| 成本分解与年度路径 | `costs/` |
| 回归结果与诊断 | `regressions/` |
| 备选回归与中美德比较 | `model_comparison/`、`source_comparison/` |
| CGE模型、输入与最终输出 | `cge/` |
| 正文绘图代码、五张最终图 | `plotting/`、`Figures/` |
| 本次复现验证情况 | `docs/REPRODUCIBILITY.md` |


