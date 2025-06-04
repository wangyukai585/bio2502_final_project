# output.py

import csv  # 用于写 CSV 文件

def write_csv(chain, filename='alignment.csv'):
    """
    将 anchor 链以 CSV 格式输出，便于查看比对位置分布

    参数：
        chain: 一组 (ref_pos, query_pos) 的 anchor 对
        filename: 输出文件名（默认为 'alignment.csv'）
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ref_pos', 'query_pos'])  # 写入表头
        for r, q in chain:
            writer.writerow([r, q])  # 写入每个 anchor 对


def write_paf(query_name, query_len, query_start, query_end,
              ref_name, ref_len, ref_start, ref_end,
              n_match, aln_len, mapq, filename='alignment.paf'):
    """
    输出简化版的 PAF 格式行（Pairwise Alignment Format）

    参数：
        query_name: 查询序列名称（例如 'query1'）
        query_len: 查询序列总长度
        query_start, query_end: 查询中匹配的起始与结束位置
        ref_name: 参考序列名称（例如 'ref1'）
        ref_len: 参考序列总长度
        ref_start, ref_end: 参考中匹配的起始与结束位置
        n_match: 匹配碱基数（粗略用 anchor 数目代替）
        aln_len: 比对长度（一般为 ref_end - ref_start）
        mapq: mapping quality 映射质量（目前为固定值,由于计算质量较为繁琐，在此不作计算）
        filename: 输出文件名（默认 'alignment.paf'）
    """
    with open(filename, 'w') as f:
        # 按照标准 PAF 格式字段顺序输出
        f.write(f"{query_name}\t{query_len}\t{query_start}\t{query_end}\t+\t"
                f"{ref_name}\t{ref_len}\t{ref_start}\t{ref_end}\t"
                f"{n_match}\t{aln_len}\t{mapq}\n")
