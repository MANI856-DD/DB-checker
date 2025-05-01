
import streamlit as st
import pandas as pd

st.set_page_config(page_title="DB品番検索", layout="wide")  # ← これが最初の Streamlit コマンドであることが重要

# --- パスワード保護設定 ---
PASSWORD = "8592"
password_entered = st.text_input("🔐 パスワードを入力してください", type="password")

if password_entered != PASSWORD:
    st.warning("正しいパスワードを入力してください")
    st.stop()

# --- 通常のアプリ開始 ---
df = pd.read_csv("Book2_fixed.csv", encoding="utf-8-sig")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #f6f8f9;
            font-family: 'Segoe UI', sans-serif;
            color: #2c3e50;
        }
        h1 {
            color: #daaa00;
            font-weight: 700;
        }
        .stDataFrame table {
            font-size: 14px;
            background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>DB品番検索</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    part_number = st.text_input("品番を入力（例: BC-31）")
with col2:
    shape_input = st.text_input("作業部形状を入力（例: Flame, Round, Taper）")
with col3:
    diameter_input = st.number_input("最大径を mm 単位で入力（例：1.8）", min_value=0.0, step=0.01)
    tolerance = st.slider("許容範囲 ± (mm)", 0.0, 0.5, 0.1)

if part_number or diameter_input > 0 or shape_input:
    df_filtered = df.copy()
    if part_number:
        df_filtered = df_filtered[df_filtered["品番"].astype(str).str.contains(part_number, na=False)]
    if diameter_input > 0:
        df_filtered = df_filtered[df_filtered["最大径"].between(diameter_input - tolerance, diameter_input + tolerance)]
    if shape_input:
        df_filtered = df_filtered[df_filtered["作業部形状"].astype(str).str.contains(shape_input, na=False)]

    if "材料/結合形式" in df_filtered.columns:
        df_filtered = df_filtered.drop(columns=["材料/結合形式"])

    styled_df = df_filtered.style.set_properties(
        subset=["品番", "最大径"],
        **{"font-weight": "bold"}
    )

    st.write(f"{len(df_filtered)} 件ヒットしました：")
    st.dataframe(styled_df, use_container_width=True)
