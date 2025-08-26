
def generate_single_story(char_name, event_name, dev_name, characters, events, developments):
    """生成單角色背景故事，帶有數值變化"""
    char = characters[characters["name"] == char_name].iloc[0]
    event = events[events["event"] == event_name].iloc[0]
    dev = developments[developments["development"] == dev_name].iloc[0]

    # 初始數值
    loyalty = 50
    emotion = 50

    # 應用事件影響
    loyalty += int(event["effect_loyalty"])
    emotion += int(event["effect_emotion"])

    # 應用發展影響
    loyalty += int(dev["stance_shift"])
    emotion += int(dev["emotion_shift"])

    results = []

    # 正向版本：數值偏高
    pos_story = (
        f"【正向版本】 {char['name']}（{char['role']}，{char['age']}歲，性格：{char['personality']}），"
        f"在經歷「{event['event']}」後，逐漸展現出堅韌與希望，"
        f"最終走向「{dev['development']}」。"
        f"\n➡ 忠誠度: {loyalty + 10}，情緒值: {emotion + 10}（積極提升）"
    )
    results.append(pos_story)

    # 負向版本：數值偏低
    neg_story = (
        f"【負向版本】 {char['name']}（{char['role']}，{char['age']}歲，性格：{char['personality']}），"
        f"在經歷「{event['event']}」後，內心逐漸崩潰，陷入陰影，"
        f"雖然仍走向「{dev['development']}」，卻帶著矛盾與痛苦。"
        f"\n➡ 忠誠度: {loyalty - 10}，情緒值: {emotion - 10}（受創下降）"
    )
    results.append(neg_story)

    return results


def generate_dual_story(char1_name, char2_name, event_name, dev_name, characters, events, developments):
    """生成雙角色互動故事，帶有數值變化"""
    c1 = characters[characters["name"] == char1_name].iloc[0]
    c2 = characters[characters["name"] == char2_name].iloc[0]
    event = events[events["event"] == event_name].iloc[0]
    dev = developments[developments["development"] == dev_name].iloc[0]

    # 初始數值
    trust = 50
    conflict = 20

    # 事件影響
    trust += int(event["effect_loyalty"])
    conflict += abs(int(event["effect_emotion"])) // 2  # 情緒波動會增加衝突

    # 發展影響
    trust += int(dev["stance_shift"])
    conflict += abs(int(dev["emotion_shift"])) // 2

    results = []

    # 正向版本：合作加強
    pos_story = (
        f"【正向版本】 {c1['name']}（{c1['role']}，{c1['age']}歲）"
        f" 與 {c2['name']}（{c2['role']}，{c2['age']}歲），"
        f"在「{event['event']}」後彼此信任增加，並肩前行，"
        f"最終共同達成「{dev['development']}」。"
        f"\n➡ 信任度: {trust + 15}，衝突度: {conflict - 5}（合作順利）"
    )
    results.append(pos_story)

    # 負向版本：衝突增加
    neg_story = (
        f"【負向版本】 {c1['name']}（{c1['role']}，{c1['age']}歲）"
        f" 與 {c2['name']}（{c2['role']}，{c2['age']}歲），"
        f"在「{event['event']}」後逐漸產生隔閡與矛盾，"
        f"即使走向「{dev['development']}」，卻留下裂痕。"
        f"\n➡ 信任度: {trust - 15}，衝突度: {conflict + 10}（關係惡化）"
    )
    results.append(neg_story)

    return results



