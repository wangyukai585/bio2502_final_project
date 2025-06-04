# demo.py

# 导入各个功能模块
from minimap2_simplified.minimizer import extract_minimizers
from minimap2_simplified.index import build_index
from minimap2_simplified.chain import chain_anchors
from minimap2_simplified.align import simple_sw
from minimap2_simplified.output import write_csv, write_paf
from minimap2_simplified.visualize import plot_anchors

def run_demo():
    # 定义参考序列与查询序列（toy example）
    ref = "ACGTACGTAGCTAGCTACGATCGATCGTACGTAGCTAGCTA"
    query = "GTAGCTAGCTA"

    # 参数设置：k-mer 长度 和 minimizer 窗口大小
    k, w = 5, 4

    # 第一步：构建参考序列的 minimizer 索引
    ref_index = build_index(ref, k, w)

    # 第二步：提取查询序列中的 minimizers
    query_minis = extract_minimizers(query, k, w)

    # 第三步：根据 minimizer 匹配，生成所有 anchor 对（rpos, qpos）
    anchors = []
    for kmer, qpos in query_minis:
        if kmer in ref_index:
            for rpos in ref_index[kmer]:
                anchors.append((rpos, qpos))

    # 第四步：可视化所有 anchor 分布
    plot_anchors(anchors, title="所有 anchors 分布")

    # 第五步：进行链化，找到最佳 anchor 匹配链
    best_chain = chain_anchors(anchors)

    # 可视化最佳 chain
    plot_anchors(best_chain, title="最佳 chain 分布")

    # 第六步：将 anchor 链写入 CSV 文件（用于后续分析）
    write_csv(best_chain)

    # 第七步：进行简化 Smith-Waterman 比对并输出 PAF 文件
    if best_chain:
        # 取 chain 的首尾位置，截取 ref/query 的匹配区域
        r_start, q_start = best_chain[0]
        r_end, q_end = best_chain[-1][0] + k, best_chain[-1][1] + k
        ref_sub = ref[r_start:r_end]
        query_sub = query[q_start:q_end]

        # 执行简化 SW 局部比对，得到得分
        score, _ = simple_sw(ref_sub, query_sub)

        # 写入简化 PAF 文件
        write_paf("query1", len(query), q_start, q_end,
                  "ref1", len(ref), r_start, r_end,
                  score, r_end - r_start, 60)

        print("PAF 与 CSV 文件已输出。")
    else:
        print("未发现匹配 chain，可能无明显匹配区域。")

# 脚本入口
if __name__ == '__main__':
    run_demo()
