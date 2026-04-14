from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 创建数据库引擎 (在当前目录下生成 db 文件)
engine = create_engine('sqlite:///double11_2025.db', echo=True)
Base = declarative_base()

# 2. 定义商品表
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    original_price = Column(Float)
    discount_price = Column(Float)
    brand_tier = Column(String) # 高端、中端、大众

# 3. 定义订单表
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    actual_paid = Column(Float)
    order_time = Column(DateTime)
    city_level = Column(String) # 用于分析下沉市场

# 4. 执行创建
Base.metadata.create_all(engine)
print("✅ 2025双11数据库骨架搭建完毕！")