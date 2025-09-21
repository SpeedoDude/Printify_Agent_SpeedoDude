from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import QSize

# Correctly use relative imports
from .pages.create_page import CreatePage
# ... import other pages as needed ...

from logic import Worker # Import the worker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Amazon Optimization Agent')
        self.setGeometry(100, 100, 1600, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        nav_panel = self.create_nav_panel()
        self.stacked_widget = QStackedWidget()

        # Create an instance of the CreatePage and pass a reference to this main window
        self.create_page = CreatePage(self)
        
        # Add pages to the stacked widget
        self.stacked_widget.addWidget(QWidget()) # Placeholder for Dashboard
        self.stacked_widget.addWidget(QWidget()) # Placeholder for Products
        self.stacked_widget.addWidget(self.create_page)

        main_layout.addWidget(nav_panel)
        main_layout.addWidget(self.stacked_widget)
        self.statusBar().showMessage("Ready.")

    def create_nav_panel(self):
        # ... (This function remains the same as before) ...
        nav_panel = QFrame()
        # ... (button creation and layout) ...
        return nav_panel

    def start_task(self, task_name, on_finish_callback, **kwargs):
        """
        Controller function to create and start a worker thread.
        This is the central point for all background tasks.
        """
        self.statusBar().showMessage(f"Running: {task_name}...")
        self.worker = Worker(task_name, **kwargs)
        self.worker.finished.connect(on_finish_callback)
        self.worker.log.connect(self.statusBar().showMessage)
        self.worker.start()
