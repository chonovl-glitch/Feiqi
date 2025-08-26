
from src.data_handler.preprocessing import load_data

def test_load_data():
    characters, events, developments = load_data()
    assert not characters.empty
    assert not events.empty
    assert not developments.empty
    assert "name" in characters.columns
    assert "event" in events.columns
    assert "development" in developments.columns
