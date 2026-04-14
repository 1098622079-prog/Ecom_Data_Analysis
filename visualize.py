import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# 设置中文显示（防止图表乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 提取数据
engine = create_engine('sqlite:///double11_2025.db')
df = pd.read_sql("SELECT o.actual_paid, o.city_level, p.category, p.brand_tier FROM orders o JOIN products p ON o.product_id = p.id", engine)

# 2. 开始画图
plt.figure(figsize=(12, 6))

# 图表 1：不同城市等级的消费分布（箱线图）
plt.subplot(1, 2, 1)
sns.boxplot(x='city_level', y='actual_paid', data=df)
plt.title('2025双11各级城市客单价分布')

# 图表 2：品牌档次订单量对比（饼图）
plt.subplot(1, 2, 2)
df['brand_tier'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('不同档次品牌订单占比')

plt.tight_layout()
plt.show()