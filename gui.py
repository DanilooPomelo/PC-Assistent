import sys
from pathlib import Path
from assistant import TaskManager , gui_show_all, searcher,deleter
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication , QWidget, QPushButton, QStackedWidget, QCheckBox , QComboBox, QTextEdit,QLineEdit, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem

class GuiLogic():
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.ui_path = Path(__file__).with_name("mainwindow.ui")
        self.ui_file = QFile(str(self.ui_path))
        if not self.ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
                raise RuntimeError(f"Не удалось открыть {self.ui_path}: {self.ui_file.errorString()}")
        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui_file)
        self.ui_file.close()
        self.tm = TaskManager()
        self.find_buttons()
        self.find_pages()
        self.find_enter_boxes()
        self.find_tables()

        self.btn_connect()
        self.create_task_button()
        self.search_task_btn()
        self.complete_task_btn()
        self.delete_for_task_btn()

    def one_row_table(self, table_widget, row):
        self.tasks_model = QStandardItemModel()
                            
        self.tasks_model.setHorizontalHeaderLabels([
                        "ID",
                        "Title",
                        "Text",
                        "Status",
                        "Priority"
                                ])
                            
                          
                
         
        row = self.tasks_model.appendRow([
            QStandardItem(str(row["id"])),
            QStandardItem(row['title']),
            QStandardItem(row['text']),
            QStandardItem(row['status']),
            QStandardItem(row['priority'])
            ])
        if table_widget is not None:
            table_widget.setModel(self.tasks_model)

    def uni_show_table(self,table_widget,rows):
        self.tasks_model = QStandardItemModel()
                    
        self.tasks_model.setHorizontalHeaderLabels([
                "ID",
                "Title",
                "Text",
                "Status",
                "Priority"
                        ])
                    
                  
        
        for row in rows: 
            self.tasks_model.appendRow([
            QStandardItem(str(row["id"])),
            QStandardItem(row['title']),
            QStandardItem(row['text']),
            QStandardItem(row['status']),
            QStandardItem(row['priority'])
                 ])
        if table_widget is not None:
            table_widget.setModel(self.tasks_model)

    
    def find_buttons(self):
        if self.window is None:
            raise RuntimeError(self.loader.errorString())
        self.task_button = self.window.findChild(QPushButton, "tasks_button")
        self.note_button = self.window.findChild(QPushButton, "note_button")
        self.settings_button = self.window.findChild(QPushButton, "settings_button")
        self.exit_button = self.window.findChild(QPushButton, "exit_button") 
        self.menu_btn_create_task = self.window.findChild(QPushButton, "menu_btn_create_task")
        self.menu_btn_search_task =self.window.findChild(QPushButton, "menu_btn_search_task")
        self.menu_btn_show_all_tasks = self.window.findChild(QPushButton, "menu_btn_show_all_tasks")
        self.menu_btn_complete_tasks = self.window.findChild(QPushButton, "menu_btn_complete_tasks")
        self.menu_btn_delete_tasks = self.window.findChild(QPushButton, "menu_btn_delete_tasks")
        self.menu_btn_deadline_tasks = self.window.findChild(QPushButton, "menu_btn_deadline_tasks")
        self.menu_btn_editor_tasks = self.window.findChild(QPushButton, "menu_btn_editor_tasks")
        self.menu_btn_back_tasks = self.window.findChild(QPushButton, "menu_btn_back_tasks")
        self.menu_btn_create_note = self.window.findChild(QPushButton, "menu_btn_create_note")
        self.menu_btn_search_note = self.window.findChild(QPushButton, "menu_btn_search_note")
        self.menu_btn_show_all_notes = self.window.findChild(QPushButton, "menu_btn_show_all_notes")
        self.menu_btn_delete_note = self.window.findChild(QPushButton, "menu_btn_delete_note")
        self.menu_btn_back_note = self.window.findChild(QPushButton, "menu_btn_back_note")
        self.menu_btn_back_settings = self.window.findChild(QPushButton, "menu_btn_back_settings")
        self.btn_show_all_tasks = self.window.findChild(QPushButton, "btn_show_all_tasks")
        self.btn_show_completed_tasks = self.window.findChild(QPushButton, "btn_show_completed_tasks")
        self.btn_show_in_process_tasks = self.window.findChild(QPushButton, "btn_show_in_process_tasks")
        self.back_from_show_all_task_page = self.window.findChild(QPushButton, "back_from_show_all_task_page")
        self.task_btn_for_search = self.window.findChild(QPushButton, "task_btn_for_search")
        self.btn_push_for_complet_task = self.window.findChild(QPushButton, "btn_push_for_complet_task")
        self.delete_task_btn = self.window.findChild(QPushButton, "delete_task_btn")
        if self.delete_task_btn is None:
            raise RuntimeError("delete_task_btn")
        if self.menu_btn_search_task is None:
            raise RuntimeError("self.menu_btn_search_task")
        if self.menu_btn_show_all_tasks is None:
            raise RuntimeError("self.menu_btn_show_all_tasks")
        if self.menu_btn_complete_tasks is None:
            raise RuntimeError("self.menu_btn_complete_tasks")
        if self.menu_btn_delete_tasks is None:
            raise RuntimeError("self.menu_btn_delete_tasks")
        if self.menu_btn_deadline_tasks is None:
            raise RuntimeError("self.menu_btn_deadline_tasks")
        if self.menu_btn_editor_tasks is None:
            raise RuntimeError("self.menu_btn_editor_tasks")
        if self.menu_btn_back_tasks is None:
            raise RuntimeError("self.menu_btn_back_tasks")
        if self.menu_btn_create_note is None:
            raise RuntimeError("self.menu_btn_create_note")
        if self.menu_btn_search_note is None:
            raise RuntimeError("self.menu_btn_search_note")
        if self.menu_btn_show_all_notes is None:
            raise RuntimeError("self.menu_btn_show_all_notes")
        if self.menu_btn_delete_note is None:
            raise RuntimeError("self.menu_btn_delete_note")
        if self.menu_btn_back_note is None:
            raise RuntimeError("self.menu_btn_back_note")
        if self.menu_btn_back_settings is None:
            raise RuntimeError("self.menu_btn_back_settings")
        if self.btn_show_all_tasks is None:
            raise RuntimeError("self.btn_show_all_tasks")
        if self.btn_show_completed_tasks is None:
            raise RuntimeError("self.btn_show_completed_tasks")
        if self.btn_show_in_process_tasks is None:
            raise RuntimeError("self.btn_show_in_process_tasks")
        if self.back_from_show_all_task_page is None:
            raise RuntimeError("self.back_from_show_all_task_page")
        if self.task_btn_for_search is None:
            raise RuntimeError("self.task_btn_for_search")
        if self.btn_push_for_complet_task is None:
            raise RuntimeError("self.btn_push_for_complet_task")
        if self.menu_btn_create_task is None:
            raise RuntimeError("")
        if self.task_button is None:
            raise RuntimeError("")
        if self.note_button is None:
            raise RuntimeError("")
        if self.settings_button is None:
            raise RuntimeError("")
        if self.exit_button is None:
            raise RuntimeError("")
        self.create_task_btn = self.window.findChild(QPushButton,"create_task_btn")
        if self.create_task_btn is None:
            raise RuntimeError("")
    def find_tables(self):
        self.show_delite_task_table = self.window.findChild(QTableView, "show_delite_task_table")
        self.show_all_tasks_table = self.window.findChild(QTableView, "show_all_tasks_table")
        self.table_result_task_serach = self.window.findChild(QTableView, "table_result_task_serach")
        self.table_fo_result_complete_task = self.window.findChild(QTableView, "table_fo_result_complete_task")
        self.table_for_create_task = self.window.findChild(QTableView, "table_for_create_task")
    def find_enter_boxes(self):
        self.get_task_id_for_delite = self.window.findChild(QLineEdit, "get_task_id_for_delite")
        if self.get_task_id_for_delite is None:
            raise RuntimeError("get_task_id_for_delite")
        self.tasks_sercher_text = self.window.findChild(QLineEdit, "tasks_sercher_text")
        if self.tasks_sercher_text is None:
            raise RuntimeError("self.tasks_sercher_text")
        self.get_id_for_complete_task = self.window.findChild(QLineEdit, "get_id_for_complete_task")
        if self.get_id_for_complete_task is None:
            raise RuntimeError("get_id_for_complete_task")

        self.task_title = self.window.findChild(QLineEdit, "task_title")
        if self.task_title is None:
            raise RuntimeError("not found task_title")
        self.task_text = self.window.findChild(QTextEdit, "task_text")
        if self.task_text is None:
            raise RuntimeError("not found task_text")
        self.priority_box = self.window.findChild(QComboBox, "priority_box")
        if self.priority_box is None:
            raise RuntimeError("not found priority_box")
        self.everyday_box = self.window.findChild(QCheckBox, "everyday_box")
        if self.everyday_box is None:
            raise RuntimeError("not found everday_box")
    def find_pages(self):
        self.main_show_all_tasks_btn_page = self.window.findChild(QWidget, "main_show_all_tasks_btn_page")
        self.complete_tasks_page =self.window.findChild(QWidget, "complete_tasks_page")
        self.search_tasks_page = self.window.findChild(QWidget, "search_tasks_page")
        self.show_all_tasks_page = self.window.findChild(QWidget, "show_all_tasks_page")
        self.main_logick_stackpages = self.window.findChild(QStackedWidget, "main_logick_stackpages")
        self.pages_stack = self.window.findChild(QStackedWidget, "pages_stack")
        self.main_tasks_menu_page = self.window.findChild(QWidget, "main_tasks_menu_page")
        self.main_menu_page = self.window.findChild(QWidget, "main_menu_page")
        self.main_notes_menu_page = self.window.findChild(QWidget, "main_notes_menu_page")
        self.main_settings_menu_page = self.window.findChild(QWidget, "main_settings_menu_page")
        self.tasks_page = self.window.findChild(QWidget, "tasks_page")
        self.notes_page = self.window.findChild(QWidget, "notes_page")
        self.settings_page = self.window.findChild(QWidget, "settings_page")
        self.task_deleter_page = self.window.findChild(QWidget, "task_deleter_page")
        if self.task_deleter_page is None:
            raise RuntimeError("task_deleter_page")
        if self.main_show_all_tasks_btn_page is None:
            raise RuntimeError("self.main_show_all_tasks_btn_page")
        if self.show_all_tasks_page is None:
            raise RuntimeError("self.show_all_tasks_page")
        if self.search_tasks_page is None:
            raise RuntimeError("self.search_tasks_page")
        if self.complete_tasks_page is None:
            raise RuntimeError("self.complete_tasks_page")
        if self.main_tasks_menu_page is None:
            raise RuntimeError("main task menu pages")
        if self.main_menu_page is None:
            raise RuntimeError("main menu page")
        if self.main_notes_menu_page is None:
            raise RuntimeError("notes main menu")
        if self.main_settings_menu_page is None:
            raise RuntimeError("settings main menu")
        if self.main_logick_stackpages is None:
            raise RuntimeError("Не найден main_logick pages")
        if self.pages_stack is None:
            raise RuntimeError("Не найден pages_stack")
        if self.tasks_page is None:
            raise RuntimeError("Не найдена tasks_page")
        if self.notes_page is None:
            raise RuntimeError("Не найдена notes_page")
        if self.settings_page is None:
            raise RuntimeError("Не найдена settings_page")

    def page_opener(self, stack, main):
        if stack is None:
            raise RuntimeError(f"Не найден {[stack]}")
            
        if main is None:
            raise RuntimeError(f"Не найдена {[main]}")
            
        stack.setCurrentWidget(main)

    
    def btn_connect(self ):
        if self.exit_button is not None:
            self.exit_button.clicked.connect(self.window.close)
        if self.task_button is not None:
           self.task_button.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages, self.main_tasks_menu_page))
        if self.note_button is not None:
            self.note_button.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages, self.main_notes_menu_page))
        if self.settings_button is not None:
            self.settings_button.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages, self.main_settings_menu_page))
        if self.menu_btn_create_task is not None:
            self.menu_btn_create_task.clicked.connect(lambda:self.page_opener( self.pages_stack, self.tasks_page))
        if self.menu_btn_search_task is not None:
            self.menu_btn_search_task.clicked.connect(lambda: self.page_opener(self.pages_stack, self.search_tasks_page))
        if self.menu_btn_show_all_tasks is not None:
            self.menu_btn_show_all_tasks.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages , self.main_show_all_tasks_btn_page))
        if self.menu_btn_back_tasks is not None:
            self.menu_btn_back_tasks.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages, self.main_menu_page))
        if self.back_from_show_all_task_page is not None:
            self.back_from_show_all_task_page.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages, self.main_tasks_menu_page))
        if self.menu_btn_back_note is not None:
            self.menu_btn_back_note.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages, self.main_menu_page))
        if self.menu_btn_back_settings is not None:
            self.menu_btn_back_settings.clicked.connect(lambda: self.page_opener(self.main_logick_stackpages, self.main_menu_page))
        if self.btn_show_all_tasks is not None:
            self.btn_show_all_tasks.clicked.connect(lambda: self.page_opener(self.pages_stack, self.show_all_tasks_page))
            self.btn_show_all_tasks.clicked.connect(lambda: self.uni_show_table(self.show_all_tasks_table,(gui_show_all("tasks"))))
        if self.btn_show_completed_tasks is not None:
            self.btn_show_completed_tasks.clicked.connect(lambda: self.page_opener(self.pages_stack, self.show_all_tasks_page))
            self.btn_show_completed_tasks.clicked.connect(lambda: self.uni_show_table(self.show_all_tasks_table,(self.tm.show_by_status("Выполнено"))))
        if self.btn_show_in_process_tasks is not None:
            self.btn_show_in_process_tasks.clicked.connect(lambda: self.page_opener(self.pages_stack, self.show_all_tasks_page))
            self.btn_show_in_process_tasks.clicked.connect(lambda: self.uni_show_table(self.show_all_tasks_table,(self.tm.show_by_status("в процессе"))))
        if self.menu_btn_complete_tasks is not None:
            self.menu_btn_complete_tasks.clicked.connect(lambda: self.page_opener(self.pages_stack, self.complete_tasks_page))
        if self.menu_btn_delete_tasks is not None:
            self.menu_btn_delete_tasks.clicked.connect(lambda: self.page_opener(self.pages_stack, self.task_deleter_page))

    
    def get_from_task_serch_btn(self):
        if self.tasks_sercher_text is None:
            return
        searcher_text = self.tasks_sercher_text.text()
        rows = searcher("tasks",searcher_text)
        self.uni_show_table(self.table_result_task_serach, rows)
    def search_task_btn(self):
        if self.task_btn_for_search is not None:
            self.task_btn_for_search.clicked.connect(self.get_from_task_serch_btn)
            

    def get_for_create_btn(self):
        if self.task_title is not None:
           title = self.task_title.text()
        if self.task_text is not None:
           text = self.task_text.toPlainText()
        if self.priority_box is not None:
            priority = self.priority_box.currentText()
        if self.everyday_box is not None:
            evereyday = self.everyday_box.isChecked()
        row = self.tm.create(title, text, priority, evereyday)
        self.one_row_table(self.table_for_create_task, row)
    def create_task_button(self):
        if self.create_task_btn is not None:
            self.create_task_btn.clicked.connect(self.get_for_create_btn)


    def complete_task_btn(self):
        if self.btn_push_for_complet_task is not None:
            self.btn_push_for_complet_task.clicked.connect(self.get_for_complete_tasks_btn)
    def get_for_complete_tasks_btn(self):
        if self.get_id_for_complete_task is None:
            return
        if self.get_id_for_complete_task is not None:
            task_id = int(self.get_id_for_complete_task.text())
            
        row = self.tm.complete_task(task_id)
        self.one_row_table(self.table_fo_result_complete_task, row)


    def get_for_task_delete_btn(self):
        if self.get_task_id_for_delite is None:
            return
        if self.get_task_id_for_delite is not None:
            task_id = int(self.get_task_id_for_delite.text())
        row = deleter("tasks", task_id)
        if row is None:
            return
        self.one_row_table(self.show_delite_task_table, row)

    def delete_for_task_btn(self):
        if self.delete_task_btn is not None:
            self.delete_task_btn.clicked.connect(self.get_for_task_delete_btn)
    def run(self):
        self.window.show()
        sys.exit(self.app.exec())


    






if __name__ == "__main__":
    gui = GuiLogic()
    gui.run()   

