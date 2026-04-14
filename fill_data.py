import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_generator import Product, Order, Base  # 导入刚才定义的骨架

engine = create_engine('sqlite:///double11_2025.db')
Session = sessionmaker(bind=engine)
session = Session()

# 1. 先准备一些具有代表性的商品
categories = {
    '美妆': [('精华液', '高端'), ('面霜', '中端'), ('洗面奶', '大众')],
    '家电': [('洗碗机', '高端'), ('电饭煲', '中端'), ('插线板', '大众')],
    '服饰': [('羊绒大衣', '高端'), ('卫衣', '中端'), ('袜子', '大众')]
}

for cat, items in categories.items():
    for name, tier in items:
        # 根据档次定原价
        base_price = 2000 if tier == '高端' else (500 if tier == '中端' else 50)
        p = Product(
            name=f"2025新款-{name}",
            category=cat,
            brand_tier=tier,
            original_price=base_price,
            discount_price=base_price * random.choice([0.7, 0.8, 0.9]) # 模拟不同折扣
        )
        session.add(p)
session.commit()

# 2. 模拟 1000 条订单
city_levels = ['一线', '二线', '三线及以下']
products = session.query(Product).all()

for _ in range(1000):
    prod = random.choice(products)
    new_order = Order(
        product_id=prod.id,
        actual_paid=prod.discount_price, # 假设实付就是折扣价
        order_time=datetime(2025, 11, 11, random.randint(0, 23), random.randint(0, 59)),
        city_level=random.choice(city_levels)
    )
    session.add(new_order)

session.commit()
print("🎉 1000条2025双11模拟业务数据已注入数据库！")