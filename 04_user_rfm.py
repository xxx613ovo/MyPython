import pandas as pd
import datetime

print(">>> Day 24: 开始 RFM 分析...")
df = pd.read_csv('clean_data.csv')

# 1. 筛选购买用户
buy_df = df[df['behavior_type'] == 'buy']

# 2. 计算 R 和 F
rfm = buy_df.groupby('user_id').agg({
    'date': 'max',      # R: 最近购买日期
    'behavior_type': 'count' # F: 购买频次
}).rename(columns={'date': 'Last_Date', 'behavior_type': 'Frequency'})

# 3. 计算 R值 (假设今天是数据里的最后一天 2014-12-19)
ref_date = pd.to_datetime('2014-12-19').date()
# 转日期格式
rfm['Last_Date'] = pd.to_datetime(rfm['Last_Date']).dt.date
rfm['Recency'] = rfm['Last_Date'].apply(lambda x: (ref_date - x).days)

# 4. 打分 (qcut 4等分)
# R越小分越高 (4,3,2,1)
# duplicates='drop' 防止数据太集中导致报错
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1], duplicates='drop')
# F越大分越高 (1,2,3,4)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])

# 5. 保存结果给 Tableau 用
rfm.to_csv('result_rfm.csv')
print("✅ RFM 计算完成！已保存为 result_rfm.csv")
print(rfm.head())