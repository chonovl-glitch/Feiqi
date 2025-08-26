
from src.data_handler.preprocessing import load_data
from src.core.generator import generate_single_story, generate_dual_story
from src.core.evaluation import generate_notes

def main():
    characters, events, developments = load_data()

    print("=== 單角色模式 ===")
    single_results = generate_single_story("荊聯鶴", "家族被誣陷滅門", "轉向復仇", characters, events, developments)
    for r in single_results:
        print(r)
    print(generate_notes("single"))

    print("\n=== 雙角色模式 ===")
    dual_results = generate_dual_story("荊聯鶴", "紅聖弓", "與盟友結識", "成為領袖", characters, events, developments)
    for r in dual_results:
        print(r)
    print(generate_notes("dual"))

if __name__ == "__main__":
    main()
