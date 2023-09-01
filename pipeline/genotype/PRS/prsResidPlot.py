import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import argparse

res = pd.read_csv("./residual.txt")
res.sort_values("PRS_RESID", ascending=False)


def plot_PRS_residuals(input_file, index_names, output_file):
    # 自定义图形参数
    plt.figure(figsize=(6, 4))  # 调整图形大小
    custom_palette = sns.color_palette("Blues_r")  # 自定义颜色调色板

    # 使用 Nature 风格的样式
    sns.set_style("whitegrid")

    # 读取数据
    res = pd.read_csv(input_file)

    # 按指定列排序
    res = res.sort_values("PRS_RESID", ascending=False)
    res.index = res.IID
    # 设置 DataFrame 的索引名称
    print("Index names in 'res':", res.index)
    # 创建图形
    ax = sns.histplot(data=res, x='PRS_RESID', #kde=True,
                      bins=500, color=custom_palette[0], linewidth=0)

    # 标记线和文字
    for i, index_name in enumerate(index_names):
        value = res.loc[index_name, "PRS_RESID"]
        label = index_name
        color = custom_palette[i % len(custom_palette)]  # 根据颜色调色板选择颜色
        plt.axvline(value, 0, 0.7, color=color,
                    linestyle='--', linewidth=1.2)  # 调整线条宽度
        plt.text(value, 0.12, label, rotation=60, fontsize=10, color=color)

    # 设置 x 轴和 y 轴标签
    plt.xlabel("PRS Residual Score", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    # 修改第一个线的颜色
    ax.lines[0].set_color('grey')

    # 移除上方和右侧的坐标轴
    sns.despine()

    # 添加图例
    plt.legend(index_names, loc='upper right', fontsize=10)

    # 调整坐标轴刻度
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # 计算 x 轴的范围
#     x_min = res['PRS_RESID'].min() - 1  # 从最小值向左扩展5
#     x_max = res['PRS_RESID'].max() + 1  # 从最大值向右扩展5

#     # 设置 x 轴范围
#     plt.xlim(x_min, x_max)
    # 保存图形
    plt.savefig(output_file, dpi=1200, bbox_inches='tight')  # 保存为高分辨率图像
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Generate and customize a PRS Residuals plot.')

    parser.add_argument('input_file', help='Input data file (CSV)')
    parser.add_argument('output_file', help='Output plot file (e.g., PNG)')
    parser.add_argument('--index_names', nargs='+',
                        help='List of index names for markers', required=True)

    args = parser.parse_args()

    # 调用绘图函数
    plot_PRS_residuals(args.input_file, args.index_names, args.output_file)


if __name__ == '__main__':
    main()
