import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
sns.set(style='dark')

def create_category(category_df):
    category = category_df.sort_values(by='count', ascending=False).copy()
    return category

def create_status(status_df):
    status = status_df.sort_values(by='count', ascending=False).copy()
    status = status.reset_index(drop=True)
    return status


category_df = pd.read_csv("dataset_category.csv")
status_df = pd.read_csv("dataset_status.csv")


st.header('Proyek Analisis Data : Order Dashboard')

st.subheader('10 Pembelian Produk Terbanyak Berdasarkan Kategori Produk')
fig, ax = plt.subplots(figsize=(10, 6))
category_data = create_category(category_df)
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

st.subheader('Perbandingan Order Berhasil dan Order Gagal')
fig, ax = plt.subplots(figsize=(8, 5))
status_data = create_status(status_df)

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
ax.set_title("Jumlah Pembelian Berhasil dan Tidak Berhasil")
st.pyplot(fig)
