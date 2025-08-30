import streamlit as st
import pandas as pd

# 你的核心模組（照原本專案結構）
from src.core.generator import generate_single_story, generate_dual_story
from src.core.evaluation import generate_notes
from src.core.visualization import build_emotion_trend_figure

# ---- 基本設定 ---------------------------------------------------------------
st.set_page_config(page_title="CharForge｜故事進展模擬", page_icon="📘", layout="wide")
st.title("CharForge｜故事進展模擬（方法2：GitHub + Streamlit Cloud）")

# ---- 資料載入（快取） -------------------------------------------------------
@st.cache_data
def load_csvs():
    chars = pd.read_csv("data/characters.csv")
    evts  = pd.read_csv("data/events.csv")
    devs  = pd.read_csv("data/developments.csv")
    return chars, evts, devs

characters, events, developments = load_csvs()

# ---- 側邊欄：欄位對應 & 版面選擇 -------------------------------------------
with st.sidebar:
    st.header("🧩 資料欄位對應")

    # 預設嘗試選到慣用欄名；若沒有，就用第 0 欄
    def pick_index(df: pd.DataFrame, name: str, fallback: int = 0) -> int:
        cols = df.columns.tolist()
        return df.columns.get_indexer([name])[0] if name in cols else fallback

    char_col = st.selectbox(
        "角色名稱欄（characters.csv）",
        characters.columns.tolist(),
        index=pick_index(characters, "name", 0),
    )
    evt_col = st.selectbox(
        "事件名稱欄（events.csv）",
        events.columns.tolist(),
        index=pick_index(events, "event", 0),
    )
    dev_col = st.selectbox(
        "發展名稱欄（developments.csv）",
        developments.columns.tolist(),
        index=pick_index(developments, "development", 0),
    )

    st.divider()
    st.header("🧭 控件擺放位置")
    layout_mode = st.radio(
        "選擇版型",
        ["側邊欄控件", "頂部三欄", "雙列（角色左／事件+發展右）"],
        index=1
    )

# ---- 選項來源（依使用者對應的欄位） ----------------------------------------
c_options = characters[char_col].astype(str).tolist()
e_options = events[evt_col].astype(str).tolist()
d_options = developments[dev_col].astype(str).tolist()

# 為了與既有視覺化函式介面相容（它預期有 event/development 欄）
events_std = events.assign(event=events[evt_col])
developments_std = developments.assign(development=developments[dev_col])

# ---- 指標（概覽） -----------------------------------------------------------
m1, m2, m3 = st.columns(3)
m1.metric("角色數", len(c_options))
m2.metric("事件數", len(e_options))
m3.metric("發展數", len(d_options))

# ---- 兩個分頁 ---------------------------------------------------------------
tab1, tab2 = st.tabs(["單角色進展", "雙角色交錯"])

# =============== 單角色 ======================================================
with tab1:
    st.subheader("單角色進展")

    # 依版面模式放控件
    if layout_mode == "側邊欄控件":
        c_name = st.sidebar.selectbox("角色", c_options, index=0 if c_options else None, key="single_c")
        e_name = st.sidebar.selectbox("事件", e_options, index=0 if e_options else None, key="single_e")
        d_name = st.sidebar.selectbox("發展", d_options, index=0 if d_options else None, key="single_d")
        place = st  # 結果放主區
    elif layout_mode == "頂部三欄":
        col1, col2, col3 = st.columns(3)
        c_name = col1.selectbox("角色", c_options, index=0 if c_options else None, key="single_c")
        e_name = col2.selectbox("事件", e_options, index=0 if e_options else None, key="single_e")
        d_name = col3.selectbox("發展", d_options, index=0 if d_options else None, key="single_d")
        place = st
    else:  # 雙列
        left, right = st.columns([1, 2])
        c_name = left.selectbox("角色", c_options, index=0 if c_options else None, key="single_c")
        e_name = right.selectbox("事件", e_options, index=0 if e_options else None, key="single_e")
        d_name = right.selectbox("發展", d_options, index=0 if d_options else None, key="single_d")
        place = st

    if place.button("生成單角進展"):
        results = generate_single_story(c_name, e_name, d_name, characters, events, developments)
        place.write("\n\n".join(results))

        place.caption("🔎 自動生成的檢視要點")
        place.json(generate_notes("single"))

        fig = build_emotion_trend_figure(events_std, developments_std, e_name, d_name)
        if fig is not None:
            place.pyplot(fig, use_container_width=True)

# =============== 雙角色 ======================================================
with tab2:
    st.subheader("雙角色交錯")

    if layout_mode == "側邊欄控件":
        c1 = st.sidebar.selectbox("角色A", c_options, index=0 if c_options else None, key="dual_c1")
        c2 = st.sidebar.selectbox("角色B", c_options, index=1 if len(c_options) > 1 else 0, key="dual_c2")
        e_name = st.sidebar.selectbox("共享事件", e_options, index=0 if e_options else None, key="dual_e")
        d_name = st.sidebar.selectbox("共享發展", d_options, index=0 if d_options else None, key="dual_d")
        place = st
    elif layout_mode == "頂部三欄":
        col1, col2, col3 = st.columns(3)
        c1 = col1.selectbox("角色A", c_options, index=0 if c_options else None, key="dual_c1")
        c2 = col1.selectbox("角色B", c_options, index=1 if len(c_options) > 1 else 0, key="dual_c2")
        e_name = col2.selectbox("共享事件", e_options, index=0 if e_options else None, key="dual_e")
        d_name = col3.selectbox("共享發展", d_options, index=0 if d_options else None, key="dual_d")
        place = st
    else:  # 雙列
        left, right = st.columns([1, 2])
        c1 = left.selectbox("角色A", c_options, index=0 if c_options else None, key="dual_c1")
        c2 = left.selectbox("角色B", c_options, index=1 if len(c_options) > 1 else 0, key="dual_c2")
        e_name = right.selectbox("共享事件", e_options, index=0 if e_options else None, key="dual_e")
        d_name = right.selectbox("共享發展", d_options, index=0 if d_options else None, key="dual_d")
        place = st

    if place.button("生成雙角交錯"):
        results = generate_dual_story(c1, c2, e_name, d_name, characters, events, developments)
        place.write("\n\n".join(results))

        place.caption("🔎 自動生成的檢視要點")
        place.json(generate_notes("dual"))

        fig = build_emotion_trend_figure(events_std, developments_std, e_name, d_name)
        if fig is not None:
            place.pyplot(fig, use_container_width=True)


