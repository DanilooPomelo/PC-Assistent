from menus import main_menu
from assistant import NoteManager, TaskManager,  settings
from storage import save_notes, save_tasks ,load_notes, load_tasks
from utils import get_int

note = NoteManager(load_notes(), save_notes)
task = TaskManager(load_tasks(), save_tasks)
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
        save_notes(note.notes)
        save_tasks(task.tasks)
        print("Все успешно сохранено, выход!")
        break