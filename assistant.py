

from models import Task, Note
from menus import main_menu, menu_p1, menu_p2, menu_p3

from utils import get_int, get_txt, waitfornext
from storage import load_notes, load_tasks, save_tasks, save_notes


tasks = load_tasks()
notes = load_notes()





def get_next_id(items):
     max_id_value = 0
     for item in items:
        if item.id > max_id_value:
            max_id_value = item.id
     return max_id_value + 1
     
next_id_task = get_next_id(tasks)
next_id_note = get_next_id(notes)


def complete_task():
    task_id = get_int(
        "Введите ID задачи, которую хотите пометить выполненной: "
    )

    for task in tasks:
        if task_id == task["id"]:
            task["status"] = "Выполнено"
            save_tasks(tasks)

            print(
                f"Статус задачи «{task['title']}» "
                f"успешно изменён на: {task['status']}"
            )
            return

    print("Задача с таким ID не найдена!")

def searcher(items, section_name):
    words = get_txt("Название для поиска: ").lower()
    found_items = []

    for item in items:
        title = item["title"].lower()
        text = item["text"].lower()

        if words in title or words in text:
            found_items.append(item)

    if not found_items:
        print(f"{section_name} не найдены. Попробуйте снова!")
        return

    print(f"--- Результаты поиска: {section_name} ---")

    for item in found_items:
        print(
            f"ID: {item['id']} | "
            f"Название: {item['title']} | "
            f"Приоритет: {priority_visual(item)}"
        )

        if "status" in item:
            print(f"Статус: {item['status']}")

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
            item.priority = "low"
            return
        elif choice == 2:
            item.priority = "medium"
            return
        elif choice == 3:
            item.priority = "high"
            return
        else:
            print ("не верный выбор!")

def priority_visual(item):
    priority_icons = {
        "low": "\U0001F7E2",
        "medium": "\U0001F7E1",
        "high": "\U0001F534",
    }

    return priority_icons.get(item['priority'], "\u26AA")

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


def show_all(items, section_name):
    if not items:
        print(f"Список {section_name} пуст!")
        return

    print(f"Список ваших {section_name}:")

    for item in items:
        line = (
            f"ID: {item['id']} | "
            f"Название: {item['title']} | "
            f"Приоритет: {priority_visual(item)}"
        )

        if items.status in item:
            line += f" | Статус: {item['status']}"

        print(line)

def deleter(items, save_function):
    item_id = get_int("Введите Id для удаления: ")
    
    for item in items:
        if item_id == item.id:
            print(f"{item.title} была успешно удалена!")
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



def settings():
    while True:
        menu_p3()
        choice = get_int("Выберите пункт: ")
        if choice == 1:
            print("NOTHONG")
            return
        elif choice == 0:
            return

class TaskManager:
    def __init__(self) -> None:
        self.tasks = []
        self.taskclass = Task
    
    
    def create(self):
        id = next_id_task
        print("Задача для создания")
        title = get_txt("Название: ")
        print("Описание для задачи!")
        text = get_txt("текст задачи: ")
        status = "в процессе"
        created_at = None
        priority = "low"
        everyday = False
        deadline = None
        new_task = self.taskclass(id,title, text, status, created_at, priority, everyday, deadline)
        priority = set_priority(new_task)
        self.tasks.append(new_task)
        #next_id_task += 1
        print(f"""
                  Задача: {new_task.title} 
                  С текстом: {new_task.text}
                  Приоритет: {priority_visual(new_task)}
                  была успешно добавлена!
                  """)
        save_tasks(self.tasks)
        waitfornext()
        return
    
    def complete_task(self):
        task_id = get_int(
        "Введите ID задачи, которую хотите пометить выполненной: "
    )

        for task in self.tasks:
            if task_id == task.id:
                task.status = "Выполнено"
                save_tasks(self.tasks)

            print(
                    f"Статус задачи «{task.title}» "
                    f"успешно изменён на: {task.status}"
                )
            return

        print("Задача с таким ID не найдена!")


    def logic_p2(self):
        while True:
            menu_p2()
            choice = get_int("Выберите пункт: ")
            if choice == 1:
                self.create()
            elif choice == 2:
                show_all(self.tasks, "Задачи")
                waitfornext()
            elif choice == 3:
                self.complete_task()
                waitfornext()
            elif choice == 4:
                deleter(tasks, save_tasks(self.tasks))
                waitfornext()
            elif choice == 5:
                return
            else:
                print("неверный ввод!")