
st.sidebar.success("這是 pages/3_資料維護.py")

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="資料維護｜新增角色", page_icon="📝", layout="wide")
st.title("資料維護｜新增角色")

# ---- 找資料夾（與主程式相同的尋路邏輯） -----------------------------------
def find_data_dir() -> Path:
    base = Path(__file__).resolve().parent.parent  # pages/ 的上一層 = charforge_01
    candidates = [
        base / "data",
        base.parent / "data",
        base / "charforge" / "data",
        base.parent / "charforge" / "data",
    ]
    for p in candidates:
        if (p / "characters.csv").exists():
            return p
    st.error(
        "找不到資料檔資料夾（characters.csv）。\n"
        "請將 CSV 放在下列任一位置：\n"
        "- charforge_01/data/\n"
        "- ../data/\n"
        "- charforge_01/charforge/data/\n"
        "- ../charforge/data/"
    )
    st.stop()

data_dir = find_data_dir()
chars_path = data_dir / "characters.csv"

# ---- 讀取角色表 --------------------------------------------------------------
try:
    characters = pd.read_csv(chars_path)
except Exception as e:
    st.error(f"讀取 {chars_path} 失敗：{e}")
    st.stop()

# 基本欄位檢查
if "name" not in characters.columns:
    st.error("characters.csv 缺少必要欄位：name")
    st.stop()

# ---- 現況總覽 ---------------------------------------------------------------
left, right = st.columns([2, 1])
with left:
    st.subheader("角色列表")
    st.dataframe(characters, use_container_width=True, hide_index=True)
with right:
    st.metric("角色數量", len(characters))

st.divider()

# ---- 新增角色表單 ------------------------------------------------------------
st.subheader("新增角色")

with st.form("add_character_form", clear_on_submit=True):
    new_name = st.text_input("角色名稱（必填）", placeholder="例如：梁葵・安爾寧")
    # 依現有欄位動態提供額外屬性輸入（除了 name 之外）
    extra_inputs = {}
    for col in characters.columns:
        if col == "name":
            continue
        if pd.api.types.is_integer_dtype(characters[col]):
            extra_inputs[col] = st.number_input(f"{col}", step=1, value=int(characters[col].iloc[0]) if len(characters) else 0)
        elif pd.api.types.is_float_dtype(characters[col]):
            extra_inputs[col] = st.number_input(f"{col}", value=float(characters[col].iloc[0]) if len(characters) else 0.0)
        else:
            extra_inputs[col] = st.text_input(f"{col}", value=str(characters[col].iloc[0]) if len(characters) else "")

    submitted = st.form_submit_button("加入角色")
    if submitted:
        if not new_name.strip():
            st.error("請填寫角色名稱。")
        elif new_name in characters["name"].astype(str).tolist():
            st.warning("已存在同名角色。")
        else:
            new_row = {"name": new_name.strip()}
            for k, v in extra_inputs.items():
                new_row[k] = v
            characters = pd.concat([characters, pd.DataFrame([new_row])], ignore_index=True)
            try:
                characters.to_csv(chars_path, index=False)
                st.success(f"已加入角色：{new_name}（已寫入 {chars_path}）")
            except Exception as e:
                st.error(f"寫入 {chars_path} 失敗：{e}")

st.caption(
    "提醒：在 Streamlit Cloud 上，容器檔案不會永久保存。若要長久保存，請在 GitHub 編輯 CSV 後再重新部署；"
    "本頁面則很適合在本機或開發環境快速維護資料。"
)
