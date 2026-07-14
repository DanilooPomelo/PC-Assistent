from encodings.punycode import T
from random import choice
import re

from menus import main_menu, menu_p1, menu_p2, menu_p3

from utils import get_int, get_txt, waitfornext
from storage import load_notes, load_tasks, save_tasks, save_notes


tasks = load_tasks()
notes = load_notes()


def max_id_note():
    global next_id_note
    max_id_value = 0
    for note in notes:
        if note['id'] > max_id_value:
            max_id_value = note['id']
    next_id_note = max_id_value + 1
next_id_note = 1
max_id_note()

def max_id_task():
    global next_id_task
    max_id_value = 0
    for task in tasks:
        if task['id'] > max_id_value:
            max_id_value = task['id']
    next_id_task = max_id_value + 1
next_id_task = 1
max_id_task()

def complete_task():
    task_id = get_int("Введите ID заметки которую хотите пометить выполненой: ")
    found = False
    for task in tasks:
            if task_id == task['id']:
                task['status'] = "Выполнено"
                found = True
                print(f"статус задачи: {task['title']} успешно изменен на: {task['status']}")
                save_tasks(tasks)
                break
    if not found:
            print("заметка с таким ID не найдена!")

def searcher(items, section_name):
    words = get_txt("Название для поиска: ").lower()
    searcher = []
    for item in items:
        title = item['title'].lower()
        text = item['text'].lower()
        if words in title or words in text:
            searcher.append(item)
    if not searcher:
        print(f"{section_name} не найдена попробуйте снова!")
        return
    else:
        for item in searcher:
            print(f"""
                  ---{section_name} которые удалось найти---
                  ID: {item['id']}
                  Name: {item['title']}
                  Priority: {item['priority']}
""")

def set_priority(item):
    while True:
        print("""
              Выберите приоритет выполнения задачи
          1 - низкий\U0001F7E2
          2 - средний\U0001F7E1
          3 - высокий\U0001F534
              """)
        choice = get_int("введите значение: ")
        if choice == 1:
            item['priority'] = "low"
            return
        elif choice == 2:
            item['priority'] = "medium"
            return
        elif choice == 3:
            item['priority'] = "high"
            return
        else:
            print ("не верный выбор!")

def priority_visual(item):
    
        if item['priority'] == "low":
            return("\U0001F7E2")

        elif item['priority'] == "medium":
            return("\U0001F7E1")
        elif item['priority'] == "high":
            return("\U0001F534")
        else:
            return ("\u26AA")

def create_note():
    global next_id_note
    new_note = {
    "id": next_id_note,
    "title": "",
    "text": "",
    "priority": ""
    }
    print("Заметка для создания")
    new_note['title'] = get_txt("Название: ")
    print("текст для заметки!")
    new_note['text'] = get_txt("текст заметки: ")
    set_priority(new_note)
    print(f"""
                  Заметка:   {new_note['title']} 
                  С текстом: {new_note['text']}
                  Приоритет: {priority_visual(new_note)}
                  была успешно добавлена!
""")
    next_id_note += 1
    notes.append(new_note)
    
    save_notes(notes)
    waitfornext()
    return

def create_task():
    global next_id_task
    new_task = {
            "id": next_id_task,
            "title": "",
            "text": "",
            "status": "в процессе",
            "created_at": "",
            "priority" : "",
            "everyday" : False,
            "deadline" : ""
    }
    print("Задача для создания")
    new_task['title'] = get_txt("Название: ")
    print("текст для заметки!")
    new_task['text'] = get_txt("текст задачс: ")
    set_priority(new_task)
    print(f"""
                  Задача: {new_task['title']} 
                  С текстом: {new_task['text']}
                  Приоритет: {priority_visual(new_task)}
                  была успешно добавлена!
""")
    tasks.append(new_task)
    next_id_task += 1
    save_tasks(tasks)
    waitfornext()
    return

def show_all(items, section_name):
    if not items:
        print(f"список {section_name} пуст!")
        return
    print(f"Список ваших {section_name}")
    for item in items:
        print(
             
            f"ID: {item['id']} | "
            f"Название: {item['title']} | "
            f"Приоритет: {priority_visual(item)}"
        )

def deleter(items, save_function):
    item_id = get_int("Введите Id для удаления: ")
    
    for item in items:
        if item_id == item['id']:
            print(f"{item['title']} была успешно удалена!")
            items.remove(item)
            
            save_function(items)
            return
    
    print("по данному ID ничего не найдено!")
            
def logic_p1():
    while True:
        menu_p1()
        choice = get_int("Выберите пункт: ")
        if choice == 1:
            create_note()
        elif choice == 2:
            searcher(notes, "Заметки")
            waitfornext()
        elif choice == 3:
            show_all(notes, "Заметок")
            waitfornext()
        elif choice == 4:
            deleter(notes, save_notes)
            waitfornext()
        elif choice == 5:
            return
        else:
            print("Неверный выбор!")

def logic_p2():
    while True:
        menu_p2()
        choice = get_int("Выберите пункт: ")
        if choice == 1:
            create_task()
        elif choice == 2:
            show_all(tasks, "Задачи")
        elif choice == 3:
            complete_task()
        elif choice == 4:
            deleter(tasks, save_tasks)
        elif choice == 5:
            return
        else:
            print("неверный ввод!")

def settings():
    while True:
        menu_p3()
        choice = get_int("Выберите пункт: ")
        if choice == 1:
            print("NOTHONG")
            return
        elif choice == 0:
            return
