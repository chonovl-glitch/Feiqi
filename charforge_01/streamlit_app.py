import streamlit as st
import pandas as pd

# －－－ 你的既有邏輯（保持不動） －－－
from src.data_handler.preprocessing import load_data
from src.core.generator import generate_single_story, generate_dual_story
from src.core.evaluation import generate_notes
from src.core.visualization import build_emotion_trend_figure

# －－－ 頁面設定與抬頭 －－－
st.set_page_config(page_title="CharForge：故事模擬器", page_icon="📘", layout="wide")
st.title("CharForge：故事模擬器")
st.caption("選擇角色與事件，快速產生可閱讀的故事段落與情緒變化示意。")

# －－－ 載入資料 －－－
try:
    characters, events, developments = load_data()
except Exception as e:
    st.error("資料載入失敗，請檢查 data/*.csv 與欄位名稱。")
    st.exception(e)
    st.stop()

# 基本統計
with st.container():
    colA, colB, colC = st.columns(3)
    colA.metric("角色數", len(characters))
    colB.metric("事件數", len(events))
    colC.metric("發展數", len(developments))

tab1, tab2 = st.tabs(["單角故事", "雙主角故事"])

# －－－ 單角故事 －－－
with tab1:
    st.subheader("單角故事")
    st.caption("選一位角色與其關鍵事件／推進發展，產生一段故事草稿。")

    c_options = characters["name"].tolist()
    e_options = events["event"].tolist()
    d_options = developments["development"].tolist()

    with st.form("single_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            c_name = st.selectbox("角色", c_options, help="選擇主角")
        with col2:
            e_name = st.selectbox("關鍵事件", e_options, help="觸發故事的轉機或衝突")
        with col3:
            d_name = st.selectbox("推進發展", d_options, help="事件之後的發展節點")

        submitted = st.form_submit_button("產生故事")

    if submitted:
        # 產生故事
        story_paras = generate_single_story(c_name, e_name, d_name, characters, events, developments)
        st.markdown("### 生成結果")
        st.markdown("\n\n".join(story_paras))

        # 觀察重點（以易讀條列呈現）
        st.markdown("### 觀察重點")
        notes = generate_notes("single")
        if isinstance(notes, dict):
            for k, v in notes.items():
                st.markdown(f"- **{k}**：{v}")
        else:
            st.write(notes)

        # 情緒趨勢（示意）
        fig = build_emotion_trend_figure(events, developments, e_name, d_name)
        if fig is not None:
            st.markdown("### 角色情緒變化（示意）")
            st.pyplot(fig, use_container_width=True)
            st.caption("情緒值為相對分數，用於比較事件前後的變化。")

    with st.expander("進階設定 / 除錯（可略過）"):
        st.caption("開發時使用的檢視工具：")
        st.write("角色資料（前5列）")
        st.dataframe(characters.head(), use_container_width=True)
        st.write("事件資料（前5列）")
        st.dataframe(events.head(), use_container_width=True)
        st.write("發展資料（前5列）")
        st.dataframe(developments.head(), use_container_width=True)

# －－－ 雙主角故事 －－－
with tab2:
    st.subheader("雙主角故事")
    st.caption("選擇兩位主角，設定共同經歷與推進發展，產生交錯視角的故事片段。")

    c_options = characters["name"].tolist()
    e_options = events["event"].tolist()
    d_options = developments["development"].tolist()

    with st.form("dual_form"):
        col1, col2 = st.columns(2)
        with col1:
            c1 = st.selectbox("主角A", c_options, help="第一位主角")
        with col2:
            idx_b = 1 if len(c_options) > 1 else 0
            c2 = st.selectbox("主角B", c_options, index=idx_b, h

