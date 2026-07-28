from models import Task, Note
from menus import  menu_dead_line, menu_p1, menu_p2, menu_p3, menu_show_all, task_editor
from utils import get_int, get_txt, waitfornext
from datetime import date, datetime
from storage import db
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt





console = Console()
def searcher(table, searcher_text):
    cursor = db.cursor()

    sql = f"SELECT * FROM {table}"
    cursor.execute(sql)

    rows = cursor.fetchall()
    search_value = searcher_text.strip().casefold()

    found_rows = []

    for row in rows:
        title = str(row["title"] or "").casefold()
        text = str(row["text"] or "").casefold()

        if search_value in title or search_value in text:
            found_rows.append(row)

    return found_rows
           
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
def gui_show_all(table): #ready for GUI
    cursor = db.cursor()
    sql = f"SELECT * FROM {table}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    return rows
   
        

def deleter(table, task_id):
    cursor = db.cursor()
    sql = f"SELECT * FROM {table} WHERE id = ?"
    cursor.execute(sql, (task_id,))
    row = cursor.fetchone()
    if row is None:
        return None
    sql = f"DELETE FROM {table} WHERE id = ?"
    cursor.execute(sql, (task_id,))
    db.commit()
    return row
    
           
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


    def db_updater(self, section_name, new_value,task_id):
        cursor = db.cursor()
        sql = f"UPDATE tasks SET {section_name} = ? WHERE id =?"
        cursor.execute(sql, (new_value, task_id))
        db.commit()

    def title_editor(self, row):
        new_title = Prompt.ask("New title", default=row['title'])
        self.db_updater("title" , new_title, row['id'])

    def text_editor(self, row):
        new_text = Prompt.ask("New Text", default=row['text'])
        self.db_updater("text", new_text, row['id'])
    def priority_editor(self,row):
        new_priority = set_priority()
        self.db_updater("priority", new_priority, row['id'])
    def deadline_editor(self, row):
        new_deadline = Prompt.ask("New Deadline", default=row['deadline'])
        self.db_updater("deadline", new_deadline,row['id'])
    def everyday_editor(self, row):
        print("Ежедневная задача? 1 -- да   2 -- нет")
        choice = get_int("Ввод: ")
        if choice ==1:
            evereyday = True
        elif choice ==2:
            evereyday = False
        else:
            print("неверный выбор!")
            return
        
        self.db_updater("evereyday", evereyday, row['id'])
    def logic_editor(self):
        cursor = db.cursor()
        sql = "SELECT * FROM tasks WHERE id = ?"
        id = get_int("Enter ID:  ")
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row is None:
            print("не найдено!")
            return
        task_editor()
        choice = get_int("Выберите: ")
        if choice == 1:
            self.title_editor(row)
        elif choice == 2:
            self.text_editor(row)
        elif choice == 3:
            self.priority_editor(row)
        elif choice == 4:
            self.deadline_editor(row)
        elif choice == 5:
            self.everyday_editor(row)
        elif choice == 6:
            return



    def reminder(self):
        today = datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        sql = "SELECT * FROM tasks WHERE evereyday = 1 AND (last_reminded IS NULL OR last_reminded != ?)"
        cursor.execute(sql, (today,))
        rows = cursor.fetchall()
        for row in rows:
            print("у вас невыполненое ежидневное задание!")
            print(row['title'])
            


        sql = "UPDATE tasks SET last_reminded = ? WHERE evereyday = 1 AND (last_reminded IS NULL OR last_reminded != ?)"
        
        cursor.execute(sql, (today, today))
        db.commit()
    
    def create(self , title, text, priority, evereyday):
       
        cursor = db.cursor()
        status = "в процессе"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        deadline = None
        last_reminded = None
        cursor.execute("INSERT INTO tasks (title,text,status,created_at,priority,evereyday,deadline,last_reminded) VALUES (?,?,?,?,?,?,?,?)" , (title,text,status,created_at,priority,evereyday,deadline,last_reminded))
        
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_id,))
        row = cursor.fetchone()
        db.commit()
        return row
    
    def complete_task(self, task_id):
        cursor = db.cursor()

        sql = """
    UPDATE tasks
    SET status = ?
    WHERE id = ?
    """
        
            
        cursor.execute(sql, ("Выполнено", task_id))
        
        db.commit()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return row
        
        
        
        
    

    def show_by_status(self, section_status): # ready for gui
        cursor = db.cursor()
        sql = "SELECT * FROM tasks WHERE status = ? "
        cursor.execute(sql, (section_status,)) 
        rows = cursor.fetchall()
        return rows
          
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
            return rows

        return rows
        

    def add_deadline(self, new_deadline, task_id):
        

        cursor = db.cursor()

        sql = """
        SELECT *
        FROM tasks
        WHERE id = ?
        """

        cursor.execute(sql, (task_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        
        
        

        try:
            
            new_deadline = new_deadline.replace("." , "-")
            new_deadline = new_deadline.replace("/" , "-")
            new_deadline = new_deadline.replace(" " , "-")
            deadline = datetime.strptime(new_deadline , "%Y-%m-%d")
            new_deadline = deadline.strftime( "%Y-%m-%d")
            cursor.execute(
            """
            UPDATE tasks
            SET deadline = ?
            WHERE id = ?
            """,
            (new_deadline, task_id)
          )

            db.commit()

            cursor.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
          )

            return cursor.fetchone()
            


        except ValueError:
            print("Введите корректную дату! YYYY-MM-DD")
            return None
        

    
            
    

class NoteManager:
    def __init__(self) -> None:
        self.noteclass = Note
    
    def create(self, title,text, priority):
        cursor = db.cursor()
        cursor.execute("INSERT INTO notes (title,text,priority) VALUES (?,?,?)" , (title,text,priority))
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM notes WHERE id = ?" , (new_id,))
        row = cursor.fetchone()
        db.commit()

        return row
