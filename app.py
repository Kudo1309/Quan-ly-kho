import streamlit as st
import plotly.express as px
from utils.functions import load_data, save_data, nhap_hang, xuat_hang

st.set_page_config(page_title="Quản lý Kho", layout="wide")

st.title("📦 Ứng dụng Quản lý Kho Hàng")

tab1, tab2, tab3 = st.tabs(["📋 Danh sách hàng", "📥 Nhập hàng", "📤 Xuất hàng"])

with tab1:
    df = load_data()
    st.subheader("📋 Danh sách hàng hóa trong kho")

    # Bộ lọc nâng cao
    with st.expander("🔎 Tìm kiếm và Lọc nâng cao"):
        col1, col2, col3 = st.columns(3)

        with col1:
            keyword = st.text_input("🔤 Tìm theo Tên hoặc Mã hàng")
        with col2:
            loai_chon = st.selectbox("📂 Chọn loại hàng", options=["Tất cả"] + df["loai_hang"].unique().tolist())
        with col3:
            sap_xep = st.selectbox("↕️ Sắp xếp theo", ["Không", "Số lượng giảm dần", "Giá tăng dần", "Giá giảm dần"])

        col4, col5 = st.columns(2)
        with col4:
            min_gia, max_gia = st.slider("💰 Khoảng giá", int(df["gia"].min()), int(df["gia"].max()), (int(df["gia"].min()), int(df["gia"].max())))
        with col5:
            min_sl, max_sl = st.slider("📦 Số lượng tồn", int(df["so_luong"].min()), int(df["so_luong"].max()), (int(df["so_luong"].min()), int(df["so_luong"].max())))

        # Áp dụng bộ lọc
        filtered_df = df.copy()
        if keyword:
            filtered_df = filtered_df[
                filtered_df["ten_hang"].str.contains(keyword, case=False)
                | filtered_df["ma_hang"].str.contains(keyword, case=False)
            ]
        if loai_chon != "Tất cả":
            filtered_df = filtered_df[filtered_df["loai_hang"] == loai_chon]

        filtered_df = filtered_df[
            (filtered_df["gia"] >= min_gia) & (filtered_df["gia"] <= max_gia)
            & (filtered_df["so_luong"] >= min_sl) & (filtered_df["so_luong"] <= max_sl)
        ]

        # Sắp xếp nếu có chọn
        if sap_xep == "Số lượng giảm dần":
            filtered_df = filtered_df.sort_values(by="so_luong", ascending=False)
        elif sap_xep == "Giá tăng dần":
            filtered_df = filtered_df.sort_values(by="gia", ascending=True)
        elif sap_xep == "Giá giảm dần":
            filtered_df = filtered_df.sort_values(by="gia", ascending=False)

    # Hiển thị bảng dữ liệu sau lọc
    st.dataframe(filtered_df, use_container_width=True)

    with st.expander("📊 Biểu đồ tồn kho"):
        pie_data = filtered_df.groupby("loai_hang")["so_luong"].sum().reset_index()
        fig1 = px.pie(pie_data, values="so_luong", names="loai_hang", title="Tỉ lệ hàng tồn theo loại")
        st.plotly_chart(fig1, use_container_width=True)

        bar_data = filtered_df.sort_values(by="so_luong", ascending=False)
        fig2 = px.bar(bar_data, x="ten_hang", y="so_luong", color="loai_hang", title="Số lượng tồn kho theo mặt hàng")
        st.plotly_chart(fig2, use_container_width=True)


with tab2:
    st.subheader("Thêm hàng vào kho")

    ma_hang = st.text_input("Mã hàng")
    ten_hang = st.text_input("Tên hàng")
    loai_hang = st.text_input("Loại hàng")
    so_luong = st.number_input("Số lượng", min_value=1, step=1)
    gia = st.number_input("Đơn giá", min_value=0, step=1000)
    ngay_nhap = st.date_input("Ngày nhập")

    if st.button("✅ Thêm vào kho"):
        if not ma_hang or not ten_hang or not loai_hang:
            st.error("Vui lòng nhập đầy đủ thông tin mã, tên và loại hàng.")
        else:
            df = nhap_hang(ma_hang, ten_hang, loai_hang, so_luong, gia, ngay_nhap)
            save_data(df)
            st.success(f"Đã thêm {so_luong} sản phẩm '{ten_hang}' vào kho!")

with tab3:
    st.subheader("Xuất hàng khỏi kho")

    ma_xuat = st.text_input("Nhập mã hàng cần xuất")
    sl_xuat = st.number_input("Số lượng cần xuất", min_value=1, step=1)

    if st.button("📤 Xuất hàng"):
        if not ma_xuat:
            st.error("Vui lòng nhập mã hàng cần xuất.")
        else:
            try:
                df = xuat_hang(ma_xuat, sl_xuat)
                save_data(df)
                st.success(f"Đã xuất {sl_xuat} sản phẩm mã '{ma_xuat}'.")
            except ValueError as e:
                st.error(str(e))
