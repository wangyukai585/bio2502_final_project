# align.py

import numpy as np  # 导入 numpy 用于创建和操作比对矩阵

def simple_sw(ref, query, match=2, mismatch=-1, gap=-2):
    """
    执行简化版 Smith-Waterman 局部比对算法
    参数:
        ref: 参考序列（字符串）
        query: 查询序列（字符串）
        match: 匹配时加的分数（默认为 +2）
        mismatch: 不匹配时的惩罚分数（默认为 -1）
        gap: 插入/删除时的惩罚分数（默认为 -2）
    返回:
        max_score: 最优比对得分
        end_pos: 得分最高的位置 (ref_idx, query_idx)
    """

    m, n = len(ref), len(query)

    # 初始化比对矩阵 H，全为 0，大小为 (m+1) × (n+1)
    H = np.zeros((m + 1, n + 1), dtype=int)

    max_score = 0           # 记录全局最高分
    end_pos = (0, 0)        # 记录最高分对应的位置

    # 填充矩阵：从左上到右下遍历每个单元格
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            # 计算三种转移方式的得分
            diag = H[i-1][j-1] + (match if ref[i-1] == query[j-1] else mismatch)  # 对角线：匹配或不匹配
            delete = H[i-1][j] + gap     # 上方：删除 gap
            insert = H[i][j-1] + gap     # 左方：插入 gap

            # 当前单元格得分是三者中的最大值，最小不能低于 0（Smith-Waterman 局部比对特性）
            H[i][j] = max(0, diag, delete, insert)

            # 如果当前得分超过历史最高，更新记录
            if H[i][j] > max_score:
                max_score = H[i][j]
                end_pos = (i, j)

    # 返回最高得分及其位置
    return max_score, end_pos
