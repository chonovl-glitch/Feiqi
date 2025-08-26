import streamlit as st
import pandas as pd

from src.data_handler.preprocessing import load_data
from src.core.generator import generate_single_story, generate_dual_story
from src.core.evaluation import generate_notes
from src.core.visualization import build_emotion_trend_figure

st.set_page_config(page_title="CharForge｜故事進展模擬", page_icon="📘", layout="wide")
st.title("CharForge｜故事進展模擬（方法2：GitHub + Streamlit Cloud）")

characters, events, developments = load_data()

colA, colB, colC = st.columns(3)
with colA:
    st.metric("角色數", len(characters))
with colB:
    st.metric("事件數", len(events))
with colC:
    st.metric("發展數", len(developments))

tab1, tab2 = st.tabs(["單角色進展", "雙角色交錯"])

with tab1:
    st.subheader("單角色模式")
    c_options = characters["name"].tolist()
    e_options = events["event"].tolist()
    d_options = developments["development"].tolist()

    col1, col2, col3 = st.columns(3)
    with col1:
        c_name = st.selectbox("角色", c_options, index=0 if c_options else None)
    with col2:
        e_name = st.selectbox("事件", e_options, index=0 if e_options else None)
    with col3:
        d_name = st.selectbox("發展", d_options, index=0 if d_options else None)

    if st.button("生成單角故事"):
        results = generate_single_story(c_name, e_name, d_name, characters, events, developments)
        st.write("\n\n".join(results))
        st.caption("🔎 自動生成的檢視要點")
        st.json(generate_notes("single"))

        fig = build_emotion_trend_figure(events, developments, e_name, d_name)
        if fig is not None:
            st.pyplot(fig, use_container_width=True)

with tab2:
    st.subheader("雙角色模式")
    c_options = characters["name"].tolist()
    e_options = events["event"].tolist()
    d_options = developments["development"].tolist()

    col1, col2 = st.columns(2)
    with col1:
        c1 = st.selectbox("角色A", c_options, index=0 if c_options else None)
    with col2:
        c2 = st.selectbox("角色B", c_options, index=1 if len(c_options) > 1 else 0 if c_options else None)

    col3, col4 = st.columns(2)
    with col3:
        e_name = st.selectbox("共享事件", e_options, index=0 if e_options else None, key="dual_event")
    with col4:
        d_name = st.selectbox("共享發展", d_options, index=0 if d_options else None, key="dual_dev")

    if st.button("生成雙角故事"):
        results = generate_dual_story(c1, c2, e_name, d_name, characters, events, developments)
        st.write("\n\n".join(results))
        st.caption("🔎 自動生成的檢視要點")
        st.json(generate_notes("dual"))

        fig = build_emotion_trend_figure(events, developments, e_name, d_name)
        if fig is not None:
            st.pyplot(fig, use_container_width=True)
