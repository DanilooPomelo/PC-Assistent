from models import Task, Note
from menus import main_menu, menu_dead_line, menu_p1, menu_p2, menu_p3, menu_show_all
from utils import get_int, get_txt, waitfornext
from datetime import datetime




def get_next_id(items):
     max_id_value = 0
     for item in items:
        if item.id > max_id_value:
            max_id_value = item.id
     return max_id_value + 1
     
def searcher(items, section_name):
    words = get_txt("Название для поиска: ").lower()
    found_items = []

    for item in items:
        title = item.title.lower()
        text = item.text.lower()

        if words in title or words in text:
            found_items.append(item)

    if not found_items:
        print(f"{section_name} не найдены. Попробуйте снова!")
        return

    print(f"--- Результаты поиска: {section_name} ---")

    for item in found_items:
        print(
            f"ID: {item.id} | "
            f"Название: {item.title} | "
            f"Приоритет: {priority_visual(item)}"
        )

        if hasattr(item,"status"):
            print(f"Статус: {item.status}")

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

    return priority_icons.get(item.priority, "\u26AA")

def show_all(items, section_name):
    if not items:
        print(f"Список {section_name} пуст!")
        return

    print(f"Список ваших {section_name}:")

    for item in items:
        line = (
            f"ID: {item.id} | "
            f"Название: {item.title} | "
            f"Приоритет: {priority_visual(item)}"
        )

        if hasattr(item, "status"):
            line += f" | Статус: {item.status}"

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
    def __init__(self, tasks , save_function) -> None:
        self.tasks = tasks
        self.save_function = save_function
        self.taskclass = Task
    
    
    def create(self):
        new_id = get_next_id(self.tasks)
        print("Задача для создания")
        title = get_txt("Название: ")
        print("Описание для задачи!")
        text = get_txt("текст задачи: ")
        status = "в процессе"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        priority = "low"
        everyday = False
        deadline = None
        new_task = self.taskclass(new_id,title, text, status, created_at, priority, everyday, deadline)
        set_priority(new_task)
        self.tasks.append(new_task)
        
        print(f"""
                  Задача: {new_task.title} 
                  С текстом: {new_task.text}
                  Приоритет: {priority_visual(new_task)}
                  была успешно добавлена!
                  """)
        self.save_function(self.tasks)
        waitfornext()
        return
    
    def complete_task(self):
        task_id = get_int(
        "Введите ID задачи, которую хотите пометить выполненной: "
    )
        for task in self.tasks:
            if task_id == task.id:
                task.status = "Выполнено"
                self.save_function

                print(
                    f"Статус задачи «{task.title}» "
                    f"успешно изменён на: {task.status}"
                )
                return

        print("Задача с таким ID не найдена!")

    def logic_showall(self):
        choice = get_int("Ввод: ")
        if choice == 1:
            show_all(self.tasks, "Задачи")
        elif choice == 2:
            self.show_by_status("в процессе")
        elif choice == 3:
            self.show_by_status("Выполнено")

    def show_by_status(self, section_status):
        found = False
        for task in self.tasks:
            if task.status == section_status:
                found = True
                print(
            f"ID: {task.id} | "
            f"Название: {task.title} | "
            f"Статус: {task.status}"
            f"Приоритет: {priority_visual(task)}"
        )
        if not found:
            print("Нет таких задач")
        
    def remeber_deadline(self):
        today = datetime.now().strftime("%Y-%m-%d")
        for task in self.tasks:
            if task.deadline is None:
                continue
            if task.status == "Выполнено":
                continue
            if task.deadline < today:
                print(f"у вас просроченая задача! {task.title}")

    def add_deadline(self):
        print("Введите ID задачи которой желаете добавить DEAD-LINE!")
        dead_id = get_int("Ввод: ")
        found = False
        for task in self.tasks:
            if task.id == dead_id:
                found = True
                print("Введите дату дедлайна в формате yyyy-mm-dd")
                new_deadline = get_txt("Ввод: ")
                task.deadline = new_deadline
                self.save_function(self.tasks)
                print(f"Dead-line успешно установлен на {task.deadline}")
                break
        if not found:
            print("Такой задачи не существует!")
    def dead_line_logic(self):
        menu_dead_line()
        choice = get_int("Ввод: ")
        if choice == 1:
            self.add_deadline()
            waitfornext()
        elif choice == 2:
            self.remeber_deadline()
            waitfornext()
        elif choice == 3:
            return
            
                      


    def logic_p2(self):
        while True:
            menu_p2()
            choice = get_int("Выберите пункт: ")
            if choice == 1:
                self.create()
            elif choice == 2:
                searcher(self.tasks, "Задача")
                waitfornext()
            elif choice == 3:
                menu_show_all()
                self.logic_showall()
                waitfornext()
            elif choice == 4:
                self.complete_task()
                waitfornext()
            elif choice == 5:
                deleter(self.tasks, self.save_function)
                waitfornext()
            elif choice == 6:
                self.dead_line_logic()
            elif choice == 7:
                return
            else:
                print("неверный ввод!")


class NoteManager:
    def __init__(self,notes, save_function) -> None:
        self.notes = notes
        self.save_function = save_function
        self.noteclass = Note
    
    def create(self):
        new_id =get_next_id(self.notes)
        print("Название заметки!")
        title = get_txt("Название: ")
        print("Текст Заметки!")
        text = get_txt("Введите: ")
        priority = "low"
        new_note = self.noteclass(new_id, title,text,priority)
        set_priority(new_note)
        self.notes.append(new_note)
        print(f"""
                  Заметка: {new_note.title} 
                  С текстом: {new_note.text}
                  Приоритет: {priority_visual(new_note)}
                  была успешно добавлена!
                  """)
        self.save_function(self.notes)
        waitfornext()
        return



    def logic_p1(self):
        while True:
            menu_p1()
            choice = get_int("Выберите пункт: ")
            if choice == 1:
                self.create()
            elif choice == 2:
                searcher(self.notes, "Заметки")
                waitfornext()
            elif choice == 3:
                show_all(self.notes, "Заметок")
                waitfornext()
            elif choice == 4:
                deleter(self.notes, self.save_function)
                waitfornext()
            elif choice == 5:
                return
            else:
                print("Неверный выбор!")