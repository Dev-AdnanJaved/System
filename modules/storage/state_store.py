import json
import os

def load_state(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def save_state(filepath, state):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(state, f, indent=2)

def already_alerted(state, symbol, signal, candle_time):
    key = f"{symbol}_{signal}"
    return state.get(key) == candle_time

def mark_alerted(state, symbol, signal, candle_time):
    key = f"{symbol}_{signal}"
    state[key] = candle_time
