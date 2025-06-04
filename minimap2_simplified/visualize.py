# visualize.py

import matplotlib
import matplotlib.pyplot as plt

# 设置 matplotlib 支持中文字体（防止标题中中文乱码）
matplotlib.rcParams['font.sans-serif'] = ['PingFang HK']
matplotlib.rcParams['axes.unicode_minus'] = False

def plot_anchors(anchors, title="Anchor 分布图"):
    """
    将 anchor 对可视化为二维散点图，横轴是参考序列位置，纵轴是查询序列位置

    参数：
        anchors: 列表，每个元素是 (ref_pos, query_pos)
        title: 图标题（支持中文）
    """
    # 分离参考位置和查询位置
    ref_pos = [a[0] for a in anchors]
    query_pos = [a[1] for a in anchors]

    # 创建 6x6 的正方形画布
    plt.figure(figsize=(6, 6))

    # 绘制散点图（每个 anchor 一个点）
    plt.scatter(ref_pos, query_pos, alpha=0.6)

    # 添加坐标轴标签和标题
    plt.xlabel("Reference Position")  # 横轴标签
    plt.ylabel("Query Position")      # 纵轴标签
    plt.title(title)

    # 显示网格以便于观察 anchor 分布趋势
    plt.grid(True)

    # 展示图像
    plt.show()
