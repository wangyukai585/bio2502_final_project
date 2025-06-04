# Minimap2 Simplified (Python)

本项目是一个简化版的 [Minimap2](https://github.com/lh3/minimap2) 对应实现，作为BIO2502的期末项目作业。Minimap2是一个十分前沿的序列比对算法，由2018年Heng Li在Bioinformatics杂志上发表。

## 注意

README仅为最简洁的项目介绍，

为方便读者易于理解与使用本项目的python软件包，作者编写了更详细的项目报告和用户手册。

项目报告请见文档。
用户手册请见文档。


## 算法流程

- 提取 minimizer 作为种子
- 构建索引，匹配 anchor
- 动态规划链化 anchor
- Smith-Waterman base-level 比对
- 输出为 CSV / PAF
- 可视化 anchor 分布

## 快速使用

```bash
git clone https://github.com/wangyukai585/bio2502_final_project
cd minimap2_simplified
pip install -e .
python examples/demo.py  ## 仅为测试实例