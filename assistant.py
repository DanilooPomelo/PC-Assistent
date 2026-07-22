

from models import Task, Note
from menus import  menu_dead_line, menu_p1, menu_p2, menu_p3, menu_show_all
from utils import get_int, get_txt, waitfornext
from datetime import date, datetime
from storage import db





def searcher(table, section_name):
    cursor = db.cursor()
    sql = f"SELECT * FROM {table}"
    words = get_txt("Название для поиска: ").lower()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    found = False
    for row in rows:
        
        if words in row['title'].lower() or words in row['text'].lower():
            found = True
            print(f"Нашел {section_name}"
                  f"С ID: {row['id']}"
                  f"Название: {row['title']}"
                  f"Приоритет: {priority_visual(row)}")
    if not found:
        print("По вашему запросу ничего не найдено!")
        
       

def set_priority():
    while True:
        print("""
              Выберите приоритет выполнения задачи
          1 - низкий\U0001F7E2
          2 - средний\U0001F7E1
          3 - высокий\U0001F534
              """)
        choice = get_int("введите значение: ")
        if choice == 1:
            priority = "low"
            return priority
        elif choice == 2:
            priority = "medium"
            return priority
        elif choice == 3:
            priority = "high"
            return priority
        else:
            print ("не верный выбор!")

def priority_visual(item):
    priority_icons = {
        "low": "\U0001F7E2",
        "medium": "\U0001F7E1",
        "high": "\U0001F534",
    }

    return priority_icons.get(item['priority'], "\u26AA")


def show_all(table, section_name):
    cursor = db.cursor()
    sql = f"SELECT * FROM {table}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if not rows:
        print(f"Список {section_name} пуст!")
    for row in rows:
        print(f"ID: {row['id']} | "
            f"Название: {row['title']} | "
            f"Приоритет: {priority_visual(row)}")
        if "status" in row.keys():
            print(f"Статус: {row['status']}")

def deleter(table, section_name):
    cursor = db.cursor()
    item_id = get_int("Введите Id для удаления: ")
    sql = f"SELECT * FROM {table} WHERE id = ?"
    cursor.execute(sql, (item_id,))
    row = cursor.fetchone()
    if row is None:
        print("Задача с таким ID не найдена!")
        return
    sql = f"DELETE FROM {table} WHERE id = ?"
    cursor.execute(sql, (item_id,))
    db.commit()
    print(f"{section_name}, с названием {row['title']} была успешно удалена!")
    
    
            
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
    def __init__(self,) -> None:
        self.taskclass = Task
    
    def create(self):
        cursor = db.cursor()
        print("Задача для создания")
        title = get_txt("Название: ")
        print("Описание для задачи!")
        text = get_txt("текст задачи: ")
        status = "в процессе"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        priority = set_priority()
        evereyday = False
        deadline = None
        last_reminded = None
        cursor.execute("INSERT INTO tasks (title,text,status,created_at,priority,evereyday,deadline,last_reminded) VALUES (?,?,?,?,?,?,?,?)" , (title,text,status,created_at,priority,evereyday,deadline,last_reminded))
        
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_id,))
        row = cursor.fetchone()
        print(f"""
              Задача:    {row["title"]}
              С текстом: {row["text"]}
              Приоритет: {priority_visual(row)}""")
        db.commit()
        waitfornext()
        return
    
   
     
    def complete_task(self):
        task_id = get_int(
        "Введите ID задачи, которую хотите пометить выполненной: "
    )

        cursor = db.cursor()

        sql = """
    UPDATE tasks
    SET status = ?
    WHERE id = ?
    """
        
            
        cursor.execute(sql, ("Выполнено", task_id))
        if cursor.rowcount == 0:
            print("Такой задачи не существует!")
            return
        db.commit()

        print("Статус задачи успешно изменён!")
        
    def logic_showall(self):
        choice = get_int("Ввод: ")
        if choice == 1:
            show_all("tasks", "Задач")
        elif choice == 2:
            self.show_by_status("в процессе")
        elif choice == 3:
            self.show_by_status("Выполнено")

    def show_by_status(self, section_status):
        cursor = db.cursor()
        sql = "SELECT * FROM tasks WHERE status = ? "
        cursor.execute(sql, (section_status,)) 
        rows = cursor.fetchall()
        if not rows:
            print("Нет таких задач")
        for row in rows:
             print(
            f"ID: {row['id']} | "
            f"Название: {row['title']} | "
            f"Статус: {row['status']} |"
            f"Приоритет: {priority_visual(row)}"
        )
          
    def today_deadline(self):
        today = datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()

        sql = """
    SELECT *
    FROM tasks
    WHERE deadline IS NOT NULL
      AND status != ?
      AND deadline = ?
    """  
            
        cursor.execute(sql, ("Выполнено", today))
        rows = cursor.fetchall()

        if not rows:
            print("на сегодня список пуст!")
            return

        for row in rows:
             print(
            f"Сегодняшняя задача: {row['title']} | "
            f"Дедлайн: {row['deadline']}"
        )
        
    def remember_deadline(self):
        today = datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()

        sql = """
    SELECT *
    FROM tasks
    WHERE deadline IS NOT NULL
      AND status != ?
      AND deadline < ?
    """  
            
        cursor.execute(sql, ("Выполнено", today))
        rows = cursor.fetchall()

        if not rows:
            print("Просроченных задач нет!")
            return

        for row in rows:
             print(
            f"Просроченная задача: {row['title']} | "
            f"Дедлайн: {row['deadline']}"
        )

    def add_deadline(self):
        print("Введите ID задачи, которой желаете добавить DEAD-LINE!")
        dead_id = get_int("Ввод: ")

        cursor = db.cursor()

        sql = """
        SELECT *
        FROM tasks
        WHERE id = ?
        """

        cursor.execute(sql, (dead_id,))
        row = cursor.fetchone()

        if row is None:
            print("Задача с таким ID не найдена!")
            return
        
        sql = """
        UPDATE tasks
        SET deadline = ?
        WHERE id = ?
        """
        

        try:
            print("Введите дату дедлайна в формате yyyy-mm-dd")
            new_deadline = get_txt("Ввод: ")
            new_deadline = new_deadline.replace("." , "-")
            new_deadline = new_deadline.replace("/" , "-")
            new_deadline = new_deadline.replace(" " , "-")
            deadline = datetime.strptime(new_deadline , "%Y-%m-%d")
            new_deadline = deadline.strftime( "%Y-%m-%d")
            print(
           f"Dead-line для задачи «{row['title']}» "
           f"успешно установлен на {new_deadline}")
            cursor.execute(sql, (new_deadline, dead_id))
            db.commit()
        except ValueError:
            print("Введите корректную дату! YYYY-MM-DD")

        

        
        
  
    def dead_line_logic(self):
        menu_dead_line()
        choice = get_int("Ввод: ")
        if choice == 1:
            self.add_deadline()
            waitfornext()
        elif choice == 2:
            self.remember_deadline()
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
                searcher("tasks", "Задача")
                waitfornext()
            elif choice == 3:
                menu_show_all()
                self.logic_showall()
                waitfornext()
            elif choice == 4:
                self.complete_task()
                waitfornext()
            elif choice == 5:
                deleter("tasks", "Задача")
                waitfornext()
            elif choice == 6:
                self.dead_line_logic()
            elif choice == 7:
                return
            else:
                print("неверный ввод!")


class NoteManager:
    def __init__(self) -> None:
        self.noteclass = Note
    
    def create(self):
        cursor = db.cursor()
        print("Название заметки!")
        title = get_txt("Название: ")
        print("Текст Заметки!")
        text = get_txt("Введите: ")
        priority = set_priority()
        cursor.execute("INSERT INTO notes (title,text,priority) VALUES (?,?,?)" , (title,text,priority))
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM notes WHERE id = ?" , (new_id,))
        row = cursor.fetchone()
        print(f"""Заметка:    {row["title"]}
              С текстом: {row["text"]}
              Приоритет: {priority_visual(row)}""")
        db.commit()
        waitfornext()
        return



    def logic_p1(self):
        while True:
            menu_p1()
            choice = get_int("Выберите пункт: ")
            if choice == 1:
                self.create()
            elif choice == 2:
                searcher("notes", "Заметки")
                waitfornext()
            elif choice == 3:
                show_all("notes", "Заметок")
                waitfornext()
            elif choice == 4:
                deleter("notes", "Заметка")
                waitfornext()
            elif choice == 5:
                return
            else:
                print("Неверный выбор!")