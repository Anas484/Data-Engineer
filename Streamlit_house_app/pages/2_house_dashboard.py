import streamlit as st
import pandas as pd
import psycopg2
from numpy.random import default_rng as rng
import plotly.express as px
st.set_page_config(layout="wide")
st.title("Housing :blue[Dashboard] 📊")

try:
    conn = psycopg2.connect(
            host="database-1.cv8wm6u8wjf7.ap-south-1.rds.amazonaws.com",
            dbname="house",
            user="postgres",
            password="anasshafi",
            port=5432
        )
    if conn:
        st.badge("Connected", color="green")
except:
    st.badge("Disconnected", color="red")

st.write("")

with conn.cursor() as cur:
    cur.execute("select * from houses")
    data = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data,columns=columns)

col1, col2, col3 = st.columns(3)

col1.metric("Total Houses", len(df))
col2.metric("Avg Price", f"₹{df['price'].mean():,.0f}")
col3.metric("Avg Area (sqft)", f"{df['area_sqft'].mean():,.0f}")
st.write("")



col4 , col5 = st.columns(2)

bar_data = df.groupby('area_type')['price'].mean().reset_index()
fig1 = px.bar(
    bar_data,
    x="area_type",       # column name
    y="price",           # column name
    color="area_type",   # column name for color
    title="Average Price by Area Type"
)
with col4:
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig = px.scatter(df, x="area_sqft", y="price", color="area_type",title="Sqft By Price")
    fig.update_yaxes(range=[0, 1000000])  # example range
    st.plotly_chart(fig, use_container_width=True)

col6, col7 = st.columns(2)

with col6:
    fig = px.box(df, x="flattype_bhk", y=pd.to_numeric(df["price"]), color="flattype_bhk",
                                    title="Price by BHK")
    st.plotly_chart(fig, use_container_width=True)


with col7:
    fig = px.scatter(df, x="price", y="deposit", color="rentorsale",
                                        title="Rent vs Deposit")
    fig.update_yaxes(range=[0, 5000000])
    fig.update_xaxes(range=[0, 1000000])
    st.plotly_chart(fig, use_container_width=True)



fig = px.histogram(df, x="price", nbins=50, title="Price Distribution")
fig.update_xaxes(range=[0, 1000000])
st.plotly_chart(fig, use_container_width=True)