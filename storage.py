import json
from pathlib import Path
from models import Task


TASKS_FILE = Path(__file__).with_name("tasks.json")
NOTES_FILE = Path(__file__).with_name("notes.json")


def load_tasks():
    try:
        with TASKS_FILE.open("r", encoding="utf-8") as f:
            tasks = json.load(f)

        result = []

        for task in tasks:
            result.append(Task.from_dict(task))

        return result

    except FileNotFoundError:
        return []


def load_notes():
    try:
        with NOTES_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    tasks_data = []

    for task in tasks:
        tasks_data.append(task.to_dict())

    with TASKS_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)


def save_notes(notes):
    with NOTES_FILE.open("w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)