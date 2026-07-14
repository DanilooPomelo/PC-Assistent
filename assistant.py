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


def set_priority(item):
    
        print("""
              Выберите приоритет выполнения задачи
          1 - низкий🟢
          2 - средний🟡
          3 - высокий🔴
              """)
        choice = get_int("введите значение")
        if choice == 1:
            item['priority'] = "low"
            return ("вы выбрали низкий приоритет задачи🟢")
        elif choice == 2:
            item['priority'] = "medium"
            return ("🟡")
        elif choice == 3:
            item['priority'] = "high"
            return ("🔴")
        else:
            return ("не верный выбор!")


def priority_visual(item):
    
        if item['priority'] == "low":
            return("🟢")

        elif item['priority'] == "medium":
            return("🟡")
        elif item['priority'] == "high":
            return("🔴")
        else:
            return ("⚪")

def create_note():
    global next_id_note
    new_note = {
        "title" : "",
        "text" : "",
        "id" : next_id_note,
        "priority" : ""
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
            "dedaline" : ""
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


def show_all(items):
    if not items:
        print("список пуст!")
        waitfornext()
        return
    for item in items:
        print(
            f"ID: {item['id']} | "
            f"Название: {item['title']} | "
            f"Приоритет: {priority_visual(item)}"
        )
        waitfornext()


def logic_p1():
    while True:
        menu_p2()
        choice = get_int("Выберите пункт: ")
        if choice == 1:
            create_note()
        elif choice == 2:
            pass
        elif choice == 3:
            show_all(notes)
        elif choice == 4:
            pass
        elif choice == 5:
            return
        else:
            print("Неверный выбор!")
