
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_data():
    characters = pd.read_csv(os.path.join(DATA_DIR, "characters.csv"))
    events = pd.read_csv(os.path.join(DATA_DIR, "events.csv"))
    developments = pd.read_csv(os.path.join(DATA_DIR, "developments.csv"))
    return characters, events, developments

