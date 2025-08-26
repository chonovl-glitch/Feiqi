
from src.data_handler.preprocessing import load_data
from src.core.generator import generate_single_story, generate_dual_story

def test_single_story():
    characters, events, developments = load_data()
    results = generate_single_story("荊聯鶴", "家族被誣陷滅門", "轉向復仇", characters, events, developments)
    assert isinstance(results, list)
    assert len(results) == 2

def test_dual_story():
    characters, events, developments = load_data()
    results = generate_dual_story("荊聯鶴", "紅聖弓", "與盟友結識", "成為領袖", characters, events, developments)
    assert isinstance(results, list)
    assert len(results) == 2
