import pandas as pd
from sqlalchemy import create_engine

# 1. 连接数据库并读取数据
engine = create_engine('sqlite:///double11_2025.db')

# 直接用 SQL 把两张表关联起来读取到 DataFrame
query = """
SELECT o.id, o.actual_paid, o.city_level, p.name, p.category, p.brand_tier, p.original_price 
FROM orders o 
JOIN products p ON o.product_id = p.id
"""
df = pd.read_sql(query, engine)

# 2. 计算关键指标：折扣率 (实际支付 / 原价)
df['discount_rate'] = df['actual_paid'] / df['original_price']

print("--- 📊 2025双11初步分析报告 ---")

# 3. 分析不同城市的客单价（体现消费力）
city_analysis = df.groupby('city_level')['actual_paid'].mean().round(2)
print("\n📍 不同等级城市的平均客单价：")
print(city_analysis)

# 4. 分析哪个档次的品牌卖得最火（体现消费分级）
tier_counts = df['brand_tier'].value_counts()
print("\n🛍️ 不同品牌档次的订单分布：")
print(tier_counts)

# 5. 发现折扣最猛的 5 个订单
top_discounts = df.sort_values(by='discount_rate').head(5)
print("\n🔥 折扣力度最大的商品 Top 5：")
print(top_discounts[['name', 'category', 'original_price', 'actual_paid', 'discount_rate']])