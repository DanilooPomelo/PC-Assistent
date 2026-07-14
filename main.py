from menus import main_menu
from assistant import logic_p1, logic_p2, notes, settings, tasks
from storage import save_notes, save_tasks
from utils import get_int

while True:
    main_menu()
    choice = get_int("Выберите пункт: ")
    if choice == 1:
        logic_p1()
    elif choice == 2:
        logic_p2()
    elif choice == 3:
        settings()
    elif choice == 4:
        save_notes(notes)
        save_tasks(tasks)
        print("Все успешно сохранено, выход!")
        break