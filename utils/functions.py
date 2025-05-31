import pandas as pd
import streamlit as st

def load_data(path="data/kho.csv"):
    return pd.read_csv(path)

def save_data(df, path="data/kho.csv"):
    df.to_csv(path, index=False)

def nhap_hang(df, ma, sl):
    if ma in df["ma_hang"].values:
        df.loc[df["ma_hang"] == ma, "so_luong"] += sl
    else:
        st.warning("Mã hàng không tồn tại!")
    save_data(df)

def xuat_hang(df, ma, sl):
    if ma not in df["ma_hang"].values:
        st.error("Mã hàng không tồn tại!")
        return
    so_luong_hien_tai = df.loc[df["ma_hang"] == ma, "so_luong"].values[0]
    if so_luong_hien_tai < sl:
        st.error("Không đủ số lượng!")
    else:
        df.loc[df["ma_hang"] == ma, "so_luong"] -= sl
        save_data(df)
        st.success("Xuất hàng thành công!")
