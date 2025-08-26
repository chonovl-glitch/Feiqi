
from src.core.evaluation import generate_notes

def test_notes_single():
    notes = generate_notes("single")
    assert "優點" in notes
    assert "缺點" in notes
    assert "可改進方向" in notes

def test_notes_dual():
    notes = generate_notes("dual")
    assert "優點" in notes
    assert "缺點" in notes
    assert "可改進方向" in notes
