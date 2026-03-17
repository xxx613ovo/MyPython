import pandas as pd
print(">>> Day 25: 热门商品分析...")
df = pd.read_csv('clean_data.csv')

# 1. 筛选购买行为
buy_df = df[df['behavior_type'] == 'buy']

# 2. 统计销量 Top 10 商品
top_items = buy_df['item_id'].value_counts().head(10)
print("--- 销量 Top 10 商品 ID ---")
print(top_items)

# 3. 保存给 Tableau
top_items.to_frame('sales').to_csv('result_top_items.csv')
print("✅ 结果已保存为 result_top_items.csv")