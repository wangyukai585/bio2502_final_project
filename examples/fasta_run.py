# examples/fasta_run.py

# 导入核心功能模块
from minimap2_simplified.minimizer import extract_minimizers
from minimap2_simplified.index import build_index
from minimap2_simplified.chain import chain_anchors
from minimap2_simplified.align import simple_sw
from minimap2_simplified.output import write_csv, write_paf
from minimap2_simplified.visualize import plot_anchors

# 使用 Biopython 读取 FASTA
from Bio import SeqIO

def load_fasta(filepath):
    """
    读取一个 FASTA 文件，返回一个字典 {序列ID: 序列字符串}
    可支持多序列文件。
    """
    records = SeqIO.to_dict(SeqIO.parse(filepath, "fasta"))
    return {rid: str(rec.seq) for rid, rec in records.items()}


def run_fasta_alignment(ref_path, query_path, k=5, w=10):
    """
    对两个 FASTA 文件中所有序列进行全匹配比对（所有 query vs 所有 ref）

    参数：
        ref_path: 参考序列的 fasta 文件路径
        query_path: 查询序列的 fasta 文件路径
        k: k-mer 长度
        w: minimizer 滑窗大小
    """
    ref_dict = load_fasta(ref_path)
    query_dict = load_fasta(query_path)

    # 遍历所有参考序列
    for ref_id, ref_seq in ref_dict.items():
        # 构建当前参考序列的 minimizer 索引
        ref_index = build_index(ref_seq, k, w)

        # 遍历所有查询序列
        for query_id, query_seq in query_dict.items():
            # 提取查询的 minimizer
            query_minis = extract_minimizers(query_seq, k, w)

            anchors = []
            # 根据匹配的 minimizer 构造 anchors（位置对）
            for kmer, qpos in query_minis:
                if kmer in ref_index:
                    for rpos in ref_index[kmer]:
                        anchors.append((rpos, qpos))
            
            # 如果找不到任何 anchor，说明完全不匹配
            if not anchors:
                print(f"[!] No anchors found between {query_id} and {ref_id}. Skipping...")
                continue

            # 可视化所有 anchor
            plot_anchors(anchors, title=f"Anchors for {query_id} vs {ref_id}")

            # 对 anchor 做链化（最长有效匹配路径）
            chain = chain_anchors(anchors)

            # 可视化最佳链
            plot_anchors(chain, title=f"Best Chain for {query_id} vs {ref_id}")

            # 输出 CSV 格式保存 anchor 链
            write_csv(chain, filename=f"{query_id}_vs_{ref_id}.csv")

            # 如果找到链，再做局部比对并输出 PAF
            if chain:
                r_start, q_start = chain[0]
                r_end, q_end = chain[-1][0] + k, chain[-1][1] + k
                ref_sub = ref_seq[r_start:r_end]
                query_sub = query_seq[q_start:q_end]

                score, _ = simple_sw(ref_sub, query_sub)

                write_paf(query_id, len(query_seq), q_start, q_end,
                          ref_id, len(ref_seq), r_start, r_end,
                          score, r_end - r_start, 60,
                          filename=f"{query_id}_vs_{ref_id}.paf")

                print(f"[✓] {query_id} vs {ref_id} finished.")
            else:
                print(f"[✗] No chain found for {query_id} vs {ref_id}")


# 主函数入口
if __name__ == '__main__':
    # 示例：使用 examples/ref.fa 和 query.fa 进行分析
    run_fasta_alignment("examples/ref.fa", "examples/query.fa", k=4, w=4)
