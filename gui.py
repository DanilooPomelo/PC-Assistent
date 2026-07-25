import sys
from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication , QWidget, QPushButton, QStackedWidget, QCheckBox , QComboBox, QTextEdit,QLineEdit

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
        self.find_buttons()
        self.find_pages()
        self.find_enter_boxes()
        self.btn_connect()
        self.create_task_button()
    
    def find_buttons(self):
        if self.window is None:
            raise RuntimeError(self.loader.errorString())
        self.task_button = self.window.findChild(QPushButton, "tasks_button")
        self.note_button = self.window.findChild(QPushButton, "note_button")
        self.settings_button = self.window.findChild(QPushButton, "settings_button")
        self.exit_button = self.window.findChild(QPushButton, "exit_button") 
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

    def find_enter_boxes(self):
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
        self.pages_stack = self.window.findChild(QStackedWidget, "pages_stack")
        self.tasks_page = self.window.findChild(QWidget, "tasks_page")
        self.notes_page = self.window.findChild(QWidget, "notes_page")
        self.settings_page = self.window.findChild(QWidget, "settings_page")
        if self.pages_stack is None:
            raise RuntimeError("Не найден pages_stack")
        if self.tasks_page is None:
            raise RuntimeError("Не найдена tasks_page")
        if self.notes_page is None:
            raise RuntimeError("Не найдена notes_page")
        if self.settings_page is None:
            raise RuntimeError("Не найдена settings_page")

    def open_tasks_page(self):
        if self.pages_stack is None:
            raise RuntimeError("Не найден pages_stack")
    
        if self.tasks_page is None:
            raise RuntimeError("Не найдена tasks_page")
    
        self.pages_stack.setCurrentWidget(self.tasks_page)
    def open_notes_page(self):
        if self.pages_stack is None:
            raise RuntimeError("Не найден pages_stack")
        if self.notes_page is None:
            raise RuntimeError("Not found notes page")
        self.pages_stack.setCurrentWidget(self.notes_page)

    def open_settings_page(self):
        if self.pages_stack is None:
            raise RuntimeError("Не найден pages_stack")
        if self.settings_page is None:
            raise RuntimeError("Not found settings page")
        self.pages_stack.setCurrentWidget(self.settings_page)

    def btn_connect(self ):
        if self.exit_button is not None:
            self.exit_button.clicked.connect(self.window.close)
        if self.task_button is not None:
           self.task_button.clicked.connect(self.open_tasks_page)
        if self.note_button is not None:
            self.note_button.clicked.connect(self.open_notes_page)
        if self.settings_button is not None:
            self.settings_button.clicked.connect(self.open_settings_page)
    def get_for_create_btn(self):
        if self.task_title is not None:
           print(self.task_title.text())
        if self.task_text is not None:
           print(self.task_text.toPlainText())
        if self.priority_box is not None:
            print(self.priority_box.currentText())
        if self.everyday_box is not None:
            print(self.everyday_box.isChecked())

    def create_task_button(self):

        if self.create_task_btn is not None:
            self.create_task_btn.clicked.connect(self.get_for_create_btn)

       
    
    def run(self):
        self.window.show()
        sys.exit(self.app.exec())


    






if __name__ == "__main__":
    gui = GuiLogic()
    gui.run()   

