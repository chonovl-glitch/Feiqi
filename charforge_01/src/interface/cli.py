
from src.data_handler.preprocessing import load_data
from src.core.generator import generate_single_story, generate_dual_story
from src.core.evaluation import generate_notes

def run_cli():
    characters, events, developments = load_data()

    mode = input("選擇模式（1=單角色, 2=雙角色）：")

    if mode == "1":
        name = input("輸入角色名：")
        event = input("輸入事件：")
        dev = input("輸入發展：")
        results = generate_single_story(name, event, dev, characters, events, developments)
        for r in results:
            print(r)
        print(generate_notes("single"))

    elif mode == "2":
        name1 = input("輸入角色1名：")
        name2 = input("輸入角色2名：")
        event = input("輸入事件：")
        dev = input("輸入發展：")
        results = generate_dual_story(name1, name2, event, dev, characters, events, developments)
        for r in results:
            print(r)
        print(generate_notes("dual"))

