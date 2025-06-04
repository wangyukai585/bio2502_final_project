# chain.py

def deduplicate_anchors(anchors):
    """
    去除重复的 anchors（锚点对）
    输入为 [(ref_pos, query_pos), ...]
    使用 set 自动去重，再转为列表
    """
    return list(set(anchors))


def chain_anchors(anchors, max_gap=20):
    """
    将 anchors 链接成最佳匹配链（基于最长上升子序列思路）
    
    参数：
        anchors: 已提取的 (ref_pos, query_pos) 锚点对
        max_gap: 控制两个 anchor 在 ref/query 上的最大距离跳跃（用于过滤不连续）
    
    返回：
        最佳 anchor 链（最长、连续性最好的一组锚点）
    """

    # 去除重复锚点后按 ref/query 的顺序排序
    anchors = sorted(deduplicate_anchors(anchors))

    # 如果没有 anchor，直接返回空链
    if not anchors:
        return []

    n = len(anchors)
    score = [1] * n      # score[i]: 以第 i 个 anchor 结尾的最长链长度
    back = [-1] * n      # back[i]: 记录当前 anchor 最佳前驱节点

    for i in range(n):
        for j in range(max(0, i - 50), i):
            # 只有当 ref/query 都严格递增，且间距小于 max_gap 才考虑连边
            if anchors[i][0] > anchors[j][0] and anchors[i][1] > anchors[j][1] and \
                anchors[i][0] - anchors[j][0] <= max_gap and \
                anchors[i][1] - anchors[j][1] <= max_gap:
                if score[j] + 1 > score[i]:
                    score[i] = score[j] + 1
                    back[i] = j


                # 如果第 j 个 anchor 接在第 i 个 anchor 前面能得到更长链，就更新
                if score[j] + 1 > score[i]:
                    score[i] = score[j] + 1
                    back[i] = j

    # 回溯找到得分最高的链
    max_idx = score.index(max(score))
    chain = []
    while max_idx != -1:
        chain.append(anchors[max_idx])
        max_idx = back[max_idx]

    return chain[::-1]  # 返回反转后的链（从头到尾）
