import matplotlib.pyplot as plt

def plot_emotion_trend(events, developments):
    """（舊）範例：畫出角色在事件後情緒變化的趨勢（改為不直接 show）"""
    emotion_values = [0]  # 初始值
    for e in events:
        emotion_values.append(emotion_values[-1] + int(e))
    for d in developments:
        emotion_values.append(emotion_values[-1] + int(d))

    fig, ax = plt.subplots()
    ax.plot(range(len(emotion_values)), emotion_values, marker="o")
    ax.set_title("角色情緒變化")
    ax.set_xlabel("步驟")
    ax.set_ylabel("情緒值")
    return fig

def build_emotion_trend_figure(events_df, developments_df, event_name, dev_name):
    """根據表格欄位 effect_emotion / emotion_shift 建立單一事件+發展的情緒趨勢圖。"""
    try:
        ev_row = events_df[events_df["event"] == event_name].iloc[0]
        dv_row = developments_df[developments_df["development"] == dev_name].iloc[0]

        # 將字串如 '+10' 轉為整數 10
        def to_int(x):
            s = str(x).strip()
            return int(s.replace('+',''))

        base = 50
        values = [base]
        values.append(values[-1] + to_int(ev_row["effect_emotion"]))
        values.append(values[-1] + to_int(dv_row["emotion_shift"]))

        fig, ax = plt.subplots()
        ax.plot(range(len(values)), values, marker="o")
        ax.set_xticks([0,1,2], labels=["初始", f"事件：{event_name}", f"發展：{dev_name}"])
        ax.set_ylabel("情緒值")
        ax.set_title("情緒趨勢（示意）")
        return fig
    except Exception:
        return None
