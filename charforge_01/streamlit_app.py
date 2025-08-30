import streamlit as st
import pandas as pd
from pathlib import Path

# ---- 核心模組 ---------------------------------------------------------------
from src.core.generator import generate_single_story, generate_dual_story
from src.core.evaluation import generate_notes
from src.core.visualization import build_emotion_trend_figure

# ---- 基本設定 ---------------------------------------------------------------
st.set_page_config(page_title="CharForge｜故事進展模擬", page_icon="📘", layout="wide")
st.title("CharForge｜故事進展模擬")

# ---- 資料載入（快取，帶多路徑檢查） ----------------------------------------
@st.cache_data
def load_csvs():
    """嘗試多個常見位置尋找 CSV，找不到就明確提示並停止。"""
    base = Path(__file__).resolve().parent  # 這支檔所在資料夾
    candidates = [
        base / "data",
        base.parent / "data",
        base / "charforge" / "data",
        base.parent / "charforge" / "data",
    ]
    data_dir = next((p for p in candidates
                     if (p / "characters.csv").exists()
                     and (p / "events.csv").exists()
                     and (p / "developments.csv").exists()), None)
    if data_dir is None:
        st.error(
            "找不到資料檔。\n請在下列任一位置放入三個 CSV：\n"
            "- ./data/{characters.csv, events.csv, developments.csv}\n"
            "- ../data/{...}\n"
            "- ./charforge/data/{...}\n"
            "- ../charforge/data/{...}"
        )
        st.stop()

    chars = pd.read_csv(data_dir / "characters.csv")
    evts  = pd.read_csv(data_dir / "events.csv")
    devs  = pd.read_csv(data_dir / "developments.csv")
    return chars, evts, devs

# ---- 載入 ---------------------------------------------------------------
characters, events, developments = load_csvs()

# 固定欄位存在性檢查
required = {
    'characters': ['name'],
    'events': ['event'],
    'developments': ['development'],
}
missing = []
for label, cols in required.items():
    df = {'characters': characters, 'events': events, 'developments': developments}[label]
    for c in cols:
        if c not in df.columns:
            missing.append(f"{label}.{c}")
if missing:
    st.error("找不到必要欄位：" + ", ".join(missing) + "。\n請把 CSV 欄名改成固定格式：characters[name]、events[event]、developments[development]。")
    st.stop()

# ---- 數值欄位轉型（容忍 '+10' 形式） ---------------------------------------
def _to_int_series(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
        .str.strip()
        .str.replace('+', '', regex=False)
        .astype(int)
    )

events_std = events.copy()
if "effect_loyalty" in events_std.columns:
    events_std["effect_loyalty"] = _to_int_series(events_std["effect_loyalty"])
if "effect_emotion" in events_std.columns:
    events_std["effect_emotion"] = _to_int_series(events_std["effect_emotion"])

developments_std = developments.copy()
if "stance_shift" in developments_std.columns:
    developments_std["stance_shift"] = _to_int_series(developments_std["stance_shift"])
if "emotion_shift" in developments_std.columns:
    developments_std["emotion_shift"] = _to_int_series(developments_std["emotion_shift"])

# ---- 側邊欄：只保留版面選擇 -------------------------------------------------
with st.sidebar:
    st.header("🧭 控件擺放位置")
    layout_mode = st.radio(
        "選擇版型",
        ["側邊欄控件", "頂部三欄", "雙列（角色左／事件+發展右）"],
        index=1
    )

# ---- 選項來源（固定欄位） ---------------------------------------------------
c_options = characters['name'].astype(str).tolist()
e_options = events['event'].astype(str).tolist()
d_options = developments['development'].astype(str).tolist()

# ---- 總覽卡片 ---------------------------------------------------------------
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

    if place.button("生成單角故事"):
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

