import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# 设置网页配置
st.set_page_config(page_title="2025双11电商决策系统", layout="wide")
engine = create_engine('sqlite:///double11_2025.db')

st.title("🚀 2025双11电商数据管理与智能分析平台")

# --- 侧边栏：添加数据功能 ---
st.sidebar.header("➕ 业务数据录入")
with st.sidebar.form("add_order_form"):
    new_prod_id = st.number_input("商品ID", min_value=1)
    new_paid = st.number_input("实付金额", min_value=0.0)
    new_city = st.selectbox("城市等级", ["一线", "二线", "三线及以下"])
    submit_btn = st.form_submit_button("提交新订单")

    if submit_btn:
        with engine.connect() as conn:
            conn.execute(text(
                f"INSERT INTO orders (product_id, actual_paid, city_level, order_time) VALUES ({new_prod_id}, {new_paid}, '{new_city}', datetime('now'))"))
            conn.commit()
            st.success("订单已入库！")

# --- 主界面：核心看板 ---
df = pd.read_sql("SELECT o.*, p.name, p.category, p.brand_tier FROM orders o JOIN products p ON o.product_id = p.id",
                 engine)

col1, col2, col3 = st.columns(3)
col1.metric("总销售额 (GMV)", f"¥{df['actual_paid'].sum():,.2f}")
col2.metric("平均客单价", f"¥{df['actual_paid'].mean():.2f}")
col3.metric("总订单量", len(df))

# --- 数据透视：电商常用功能 ---
st.subheader("📊 实时业务分析")
tab1, tab2 = st.tabs(["品类表现", "下沉市场渗透"])

with tab1:
    cat_data = df.groupby('category')['actual_paid'].sum()
    st.bar_chart(cat_data)

with tab2:
    st.write("各级城市订单分布情况")
    city_dist = df['city_level'].value_counts()
    st.write(city_dist)

# --- 原始数据查看与搜索 ---
st.subheader("🔍 订单明细查询")
search_term = st.text_input("搜索商品名称")
if search_term:
    st.dataframe(df[df['name'].str.contains(search_term)], use_container_width=True)
else:
    st.dataframe(df.tail(10), width="stretch")

    st.subheader("📝 商品信息快捷编辑")
    # 读取商品数据
    prod_df = pd.read_sql("SELECT * FROM products", engine)

    # 使用可编辑表格
    edited_df = st.data_editor(prod_df, num_rows="dynamic", key="prod_editor")

    if st.button("保存修改到数据库"):
        edited_df.to_sql('products', engine, if_exists='replace', index=False)
        st.success("数据库已更新！")

        st.subheader("🎯 消费分级深度筛选")
        selected_tier = st.multiselect("选择品牌档次", options=df['brand_tier'].unique(),
                                       default=df['brand_tier'].unique())
        filtered_df = df[df['brand_tier'].isin(selected_tier)]

        st.line_chart(filtered_df.groupby('order_time')['actual_paid'].sum())