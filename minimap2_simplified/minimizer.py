# minimizer.py

def extract_minimizers(seq, k=5, w=10):
    """
    从序列中提取 minimizer：每个窗口中哈希值最小的 k-mer

    参数:
        seq: 输入序列（字符串，例如 DNA）
        k: k-mer 的长度（每个子串多长）
        w: 滑动窗口的大小（每次取 w 个连续 k-mer）

    返回:
        minimizers: 列表，每项为 (k-mer字符串, 在原序列中的起始位置)
    """

    minimizers = []  # 存储所有提取出的 minimizer

    # 滑动窗口在序列上移动，起点从 i 开始
    # 每次取 w 个连续的 k-mer
    for i in range(len(seq) - w - k + 2):

        # 构造当前窗口内的 w 个 k-mer
        window = [seq[i + j:i + j + k] for j in range(w)]

        # 对每个 k-mer 进行哈希，得到 (kmer, hash值)
        hashed = [(kmer, hash(kmer)) for kmer in window]

        # 找到 hash 值最小的那个 k-mer，作为 minimizer
        min_kmer, _ = min(hashed, key=lambda x: x[1])

        # 找出该 minimizer 在当前窗口中的位置，用于定位它在原始序列中的起始位置
        min_index = window.index(min_kmer)

        # 将 minimizer 及其在原序列中的位置加入结果
        minimizers.append((min_kmer, i + min_index))

    return minimizers  # 返回所有窗口提取的 minimizers
