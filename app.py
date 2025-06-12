
import streamlit as st
import pandas as pd

st.set_page_config(page_title="DB品番検索", layout="wide")

# --- データ読み込み（エンコーディング対応） ---
df = pd.read_csv("Book2_fixed.csv", encoding="cp932")

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
    shape_input = st.text_input("作業部形状を入力（例: 001, 023, 105）")
with col3:
    diameter_input = st.number_input("最大径を mm 単位で入力（例：1.8）", min_value=0.0, step=0.01)
    tolerance = st.slider("許容範囲 ± (mm)", 0.0, 0.5, 0.1)

if part_number or diameter_input > 0 or shape_input:
    df_filtered = df.copy()
    if part_number:
        df_filtered = df_filtered[
            df_filtered["品番"].astype(str).str.lower().str.contains(part_number.lower(), na=False)
        ]
    if diameter_input > 0:
        df_filtered["最大径"] = pd.to_numeric(df_filtered["最大径"], errors="coerce")
        df_filtered = df_filtered[
            df_filtered["最大径"].between(diameter_input - tolerance, diameter_input + tolerance, inclusive="both")
        ]
    if shape_input:
        shape_input_zfill = shape_input.zfill(3)
        df_filtered = df_filtered[
            df_filtered["作業部形状"].astype(str).str.zfill(3) == shape_input_zfill
        ]

    # 作業部形状を3桁ゼロ埋め表示（数値のみ）
    df_filtered["作業部形状"] = df_filtered["作業部形状"].apply(
        lambda x: f"{int(x):03}" if pd.notnull(x) and str(x).isdigit() else x
    )

    # 材料/結合形式 は除外、ISOコード列は残す
    if "材料/結合形式" in df_filtered.columns:
        df_filtered = df_filtered.drop(columns=["材料/結合形式"])

    styled_df = df_filtered.style.set_properties(
        subset=["品番", "最大径"],
        **{"font-weight": "bold"}
    ).format({
        "最大径": lambda x: f"{float(x):.2f}" if pd.notnull(x) and str(x).replace('.', '', 1).isdigit() else ""
    })

    st.write(f"{len(df_filtered)} 件ヒットしました：")
    st.dataframe(styled_df, use_container_width=True)
