import pandas as pd
from pyecharts.charts import Funnel
from pyecharts import options as opts

print(">>> Day 23: 开始漏斗分析...")
df = pd.read_csv('clean_data.csv')

# 1. 统计各环节数量
counts = df['behavior_type'].value_counts()
# 注意：你的数据里现在已经是 pv, fav, cart, buy 了
pv = counts.get('pv', 0)
cart = counts.get('cart', 0)
fav = counts.get('fav', 0)
buy = counts.get('buy', 0)

# 2. 打印转化率
print(f"总浏览量 (PV): {pv}")
print(f"总购买量 (Buy): {buy}")
if pv > 0:
    print(f"点击 -> 购买 转化率: {buy / pv:.2%}")

# 3. 制作漏斗图
data = [
    ("浏览", int(pv)),
    ("加购+收藏", int(cart + fav)),
    ("购买", int(buy))
]

c = (
    Funnel()
    .add("转化漏斗", data, gap=2, label_opts=opts.LabelOpts(position="inside"))
    .set_global_opts(title_opts=opts.TitleOpts(title="用户行为转化漏斗"))
)

c.render("result_funnel.html")
print("✅ 图表已生成：result_funnel.html")