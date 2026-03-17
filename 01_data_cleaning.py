import pandas as pd
import datetime

print(">>> Day 21: 开始清洗数据 (修复版)...")

# 1. 读取数据
df = pd.read_csv('UserBehavior.csv', header=0, nrows=1000000)

print(f"读取成功，当前列数: {len(df.columns)}")

# 2. 【核心修复】重命名列
# 你的数据只有 6 列，所以这里只给 6 个名字
if len(df.columns) == 6:
    df.columns = ['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time']
    # 删除 user_geohash (地理位置)，因为全是 NaN，分析用不上
    df = df.drop(columns=['user_geohash'])
    print("✅ 列名已修正 (6列模式)")

elif len(df.columns) == 5:
    # 万一只有 5 列 (防止意外)
    df.columns = ['user_id', 'item_id', 'behavior_type', 'item_category', 'time']
    print("✅ 列名已修正 (5列模式)")

else:
    print(f"❌ 列数异常：{len(df.columns)}，请检查文件！")
    exit()

# 3. 映射行为类型
# 原始数据：1=点击, 2=收藏, 3=加购, 4=购买
print("正在翻译行为类型...")
type_map = {1: 'pv', 2: 'fav', 3: 'cart', 4: 'buy'}
df['behavior_type'] = df['behavior_type'].map(type_map)

# 4. 时间处理
print("正在转换时间...")
df['datetime'] = pd.to_datetime(df['time'], errors='coerce')
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour

# 5. 筛选核心时间段 (去除 2014 年以外的脏数据)
# 2014版数据的核心区间是 11月18日 - 12月18日
start_date = datetime.date(2014, 11, 18)
end_date = datetime.date(2014, 12, 18)
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# 6. 保存清洗后的数据
print(f"清洗完成，剩余行数: {len(df)}")
df.to_csv('clean_data.csv', index=False)
print("✅ Day 21 任务完美结束！已保存为 clean_data.csv")
print(df.head())
