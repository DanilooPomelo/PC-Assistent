from menus import main_menu
from assistant import NoteManager, TaskManager,  settings
from utils import get_int
from storage import close_db, init_db




note = NoteManager()
task = TaskManager()
init_db()
task.remember_deadline()
task.today_deadline()
while True:
    main_menu()
    choice = get_int("Выберите пункт: ")
    if choice == 1:
        note.logic_p1()
    elif choice == 2:
        task.logic_p2()
    elif choice == 3:
        settings()
    elif choice == 4:
        close_db()
        print("Все успешно сохранено, выход!")
        break