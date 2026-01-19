import sys
import os
import json
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QLabel, QTabWidget, QTextEdit, QPushButton, QComboBox, QToolBox,
    QCheckBox, QTextBrowser, QFrame, QSplitter, QDoubleSpinBox
)
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import App state
from app_state import AppState

# Import activities
from activity1_tab import LDMTab
from activity2_tab import activity2_tab
from logs_tab import LogsTab

from gui_translations import TRANSLATIONS

# Force Qt to use X11 for compatibility
os.environ["QT_QPA_PLATFORM"] = "xcb"

# -----------------------------
# Other placeholder tabs
# -----------------------------
class SimplePlotTab(QWidget):
    def __init__(self, x, y, color="blue", title="Plot"):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        fig = Figure()
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        ax = fig.add_subplot(111)
        ax.scatter(x, y, color=color)
        ax.set_xlabel("Column 4")
        ax.set_ylabel("Column 5")
        ax.set_title(title)
        canvas.draw()


# -----------------------------
# Main Window
# -----------------------------
class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Signal only to active tab
        self.tabs.currentChanged.connect(self.on_tab_changed)

        # Initialize common environment
        self.state = AppState()

        # 🔌 CONNECT STATE SIGNALS
        self.state.groupChanged.connect(self.update_title)
        self.state.languageChanged.connect(self.translate_gui)
        # Set initial title
        self.update_title()

        # Tab 1 and 2: Interactive LDM model
        self.tab1 = LDMTab(self.state)
        self.tabs.addTab(self.tab1, "Activity 1")
        self.tab2 = activity2_tab(self.state)
        self.tabs.addTab(self.tab2, "Activity 2")
        self.tab3 = LogsTab(self.state)
        self.tabs.addTab(self.tab3, "Logs")

        self.translate_gui(self.state.language)


    def translate_gui(self, language):
        """Translate all GUI elements in the main window."""
        translations = TRANSLATIONS[language]
        self.setWindowTitle(translations["window_title"])
        self.tabs.setTabText(0, translations["activity1_tab_title"])
        self.tabs.setTabText(1, translations["activity2_tab_title"])
        self.tabs.setTabText(2, translations["logs_tab_title"])


    def update_title(self):
        """Update window title with current group."""
        self.setWindowTitle(f"Nuclear Masterclass - Group {self.state.group}")

    def on_tab_changed(self, index):
        # Disable updates in all tabs
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, "set_active"):
                tab.set_active(False)
        # Enable only the selected tab
        self.state.current_tab = self.tabs.widget(index)
        if hasattr(self.state.current_tab, "set_active"):
            self.state.current_tab.set_active(True)
        # if hasattr(self.state.current_tab, "refresh_params"):
        #     self.state.current_tab.refresh_from_params(self.state.params)
        if hasattr(self.state.current_tab, "update_load_button"):
            self.state.current_tab.update_load_button()
        if self.state.current_tab.__class__.__name__ == "activity2_tab":
            if hasattr(self.state.current_tab, "elements_box"):
                self.state.current_tab.elements_box.setCurrentIndex(8)
# -----------------------------
# Main entry point
# -----------------------------
if __name__ == "__main__":

    # Create application
    app = QApplication(sys.argv)

    # Set global font
    app.setFont(QFont("Georgia", 12))

    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())
