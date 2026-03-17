import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

print(">>> Day 22: 开始流量分析...")

# 1. 读取 Day 21 生成的完美数据
df = pd.read_csv('clean_data.csv')

# 2. 统计每小时 PV/UV
# behavior_type='count' -> PV
# user_id='nunique'     -> UV
traffic = df.groupby('hour').agg({
    'behavior_type': 'count',
    'user_id': 'nunique'
}).rename(columns={'behavior_type': 'PV', 'user_id': 'UV'})

# 3. 画图 (Pyecharts)
x_data = traffic.index.astype(str).tolist()
pv_data = traffic['PV'].tolist()
uv_data = traffic['UV'].tolist()

c = (
    Line()
    .add_xaxis(x_data)
    .add_yaxis("PV (访问量)", pv_data, is_smooth=True, yaxis_index=0)
    .add_yaxis("UV (访客数)", uv_data, is_smooth=True, yaxis_index=1)
    .extend_axis(yaxis=opts.AxisOpts(name="UV", position="right")) # 添加右轴
    .set_global_opts(
        title_opts=opts.TitleOpts(title="24小时流量趋势"),
        yaxis_opts=opts.AxisOpts(name="PV", position="left")
    )
)

# 4. 生成网页
c.render("result_traffic.html")
print("✅ 图表已生成：result_traffic.html (双击打开看看)")