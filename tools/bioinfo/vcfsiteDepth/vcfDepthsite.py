import vcf,sys

# 读取 VCF 文件
vcf_reader = vcf.Reader(open("/dev/stdin", 'r'))

# 初始化总深度和位点数量
total_depth = 0
num_variants = 0

# 遍历每个位点
for record in vcf_reader:
    # 检查位点是否有深度信息
    if 'DP' in record.INFO:
        # 提取深度信息
        depth = record.INFO['DP']
        # 累加深度信息到总深度
        total_depth += depth
        # 增加位点数量
        num_variants += 1

# 计算平均深度
average_depth = total_depth / num_variants if num_variants > 0 else 0

print("平均深度：", average_depth)
