import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
sns.set(style='dark')

def create_category(category_df):
    items_df = pd.read_csv("items_cleaned.csv")
    products_df = pd.read_csv("products_cleaned.csv")

    dataset_join_1 = pd.merge(category_df, items_df, on='order_id', how='left')
    dataset_join_2 = pd.merge(dataset_join_1, products_df, on='product_id', how='left')
    dataset_joined = dataset_join_2.copy()
    
    dataset_filtered = dataset_joined.groupby(by="product_category_name").customer_id.nunique().sort_values(ascending=False).reset_index().copy()
    dataset_filtered.columns = ["product_category_name", "count"]
    dataset_filtered = dataset_filtered.head(10)
    category = dataset_filtered.sort_values(by='count', ascending=False).copy()
    return category

def create_status(status_df):
    status_filtered = status_df.groupby(by="order_status", dropna=False).customer_id.nunique().sort_values(ascending=True).reset_index().copy()
    status_filtered.columns = ["order_status", "count"]
    status = status_filtered.sort_values(by='count', ascending=False).copy()
    status = status.reset_index(drop=True)
    return status


all_df = pd.read_csv("orders_cleaned.csv")
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'], errors='coerce')

valid_df = all_df.dropna(subset=['order_purchase_timestamp'])
missing_df = all_df[all_df['order_purchase_timestamp'].isna()]

min_date = valid_df["order_purchase_timestamp"].min().date()
max_date = valid_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = valid_df[
    (valid_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & (valid_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

main_df = pd.concat([main_df], ignore_index=True)

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

st.subheader('Diagram Seberapa Banyak Status Pesanan Produk dengan Rentang Waktu 2016-2018')
fig, ax = plt.subplots(figsize=(8, 5))
status_data = create_status(all_df)
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
ax.set_title("Jumlah dari Setiap Status Pesanan Produk Tahun 2016-2018")
st.pyplot(fig)

