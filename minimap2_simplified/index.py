# index.py

from collections import defaultdict  # defaultdict 用于自动创建空列表
from .minimizer import extract_minimizers  # 导入 minimizer 提取函数

def build_index(ref_seq, k=5, w=10):
    """
    构建参考序列的 minimizer 索引，用于快速查找匹配位置。

    参数：
        ref_seq: 参考序列（字符串）
        k: k-mer 长度（即提取的子串长度）
        w: 滑动窗口大小（每 w 个 k-mer 中取一个最小的）

    返回：
        index: dict，形式为 {k-mer: [位置列表]}，表示每个 minimizer 出现在 ref 中的位置
    """

    index = defaultdict(list)  # 初始化字典，值为列表

    # 提取参考序列中的 minimizer，并记录每个 minimizer 的位置
    for kmer, pos in extract_minimizers(ref_seq, k, w):
        index[kmer].append(pos)

    return index  # 返回构建好的索引字典
