
import random

def generate_notes(mode="single"):
    """生成三點注意項"""
    if mode == "single":
        notes = {
            "優點": random.choice(["角色背景清晰", "單線敘事合理", "情緒張力強"]),
            "缺點": random.choice(["故事過於單調", "細節不足", "結局略顯突兀"]),
            "可改進方向": random.choice(["增加角色心理描寫", "補充事件前因後果", "延展人物成長軸線"])
        }
    else:  # dual
        notes = {
            "優點": random.choice(["角色互動真實", "關係張力明顯", "雙人互補效果好"]),
            "缺點": random.choice(["互動略顯表面", "缺乏衝突細節", "角色定位模糊"]),
            "可改進方向": random.choice(["增加角色衝突", "補充合作過程", "描寫立場差異"])
        }
    return notes
