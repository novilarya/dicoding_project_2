import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
sns.set(style='dark')

def create_category(category_df):
    dataset_filtered = category_df.groupby(by="product_category_name").customer_id.nunique().sort_values(ascending=False).reset_index().copy()
    dataset_filtered.columns = ["product_category_name", "count"]
    dataset_filtered = dataset_filtered.head(10)
    category = dataset_filtered.sort_values(by='count', ascending=False).copy()
    return category

def create_status(status_df):
    status_filtered = status_df.groupby(by="order_status").customer_id.nunique().sort_values(ascending=True).reset_index().copy()
    status_filtered.columns = ["order_status", "count"]
    status = status_filtered.sort_values(by='count', ascending=False).copy()
    status = status.reset_index(drop=True)
    return status


category_df = pd.read_csv("dataset_category.csv")
status_df = pd.read_csv("dataset_status.csv")
all_df = pd.read_csv("dataset_joined.csv", parse_dates=["order_purchase_timestamp"])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & (all_df["order_purchase_timestamp"] <= str(end_date))]


st.header('Proyek Analisis Data : Order Dashboard')

st.subheader('10 Pembelian Produk Terbanyak Berdasarkan Kategori Produk')
fig, ax = plt.subplots(figsize=(10, 6))
category_data = create_category(main_df)
sns.barplot(
    x='count',
    y='product_category_name',
    data=category_data,
    ax=ax,
    order=category_data['product_category_name'],
    color='#72BCD4'
)
for i in range(len(category_data)):
    ax.text(
        category_data['count'].iloc[i] + 100,
        i,
        f'{category_data["count"].iloc[i]}',
        va='center',
        ha='left',
        fontsize=10,
        color='black'
    )
ax.set_xlabel("Jumlah")
ax.set_ylabel("Kategori Produk")
ax.set_title("Jumlah Pembelian Tiap Kategori Produk")
st.pyplot(fig)

st.subheader('Diagram Seberapa Banyak Status Pesanan Produk')
fig, ax = plt.subplots(figsize=(8, 5))
status_data = create_status(main_df)
sns.barplot(
    x='count',
    y='order_status',
    data=status_data,
    ax=ax,
    order=status_data['order_status'],
    color='#DD5746'
)
for i in range(len(status_data)):
    ax.text(
        status_data['count'].iloc[i] + 100,
        i,
        f'{status_data["count"].iloc[i]}',
        va='center',
        ha='left',
        fontsize=10,
        color='black'
    )
ax.set_xlabel("Jumlah")
ax.set_ylabel("Status Produk")
ax.set_title("Jumlah dari Setiap Status Pesanan Produk")
st.pyplot(fig)

