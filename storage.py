import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")
DATA_FILE = Path(__file__).with_name("notes.json")


def load_tasks():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def load_notes():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def save_notes(notes):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)