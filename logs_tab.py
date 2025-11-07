import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, QTimer


class EmittingStream:
    """
    Redirects all stdout/stderr text to a QTextEdit in real time.
    Optionally duplicates output to the original stream (so the console still shows it too).
    """
    def __init__(self, text_edit, orig_stream=None, show_time=True):
        self.text_edit = text_edit
        self.orig_stream = orig_stream  # keep printing to console if needed
        self.show_time = show_time

    def write(self, text):
        text = text.strip()
        if text:
            timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] " if self.show_time else ""
            formatted_text = f"{timestamp}{text}"
            # Append safely from the main thread
            QTimer.singleShot(0, lambda: self.text_edit.append(formatted_text))
        if self.orig_stream:
            # Keep console output unchanged (without timestamp)
            self.orig_stream.write(text + "\n")
            self.orig_stream.flush()

    def flush(self):
        if self.orig_stream:
            self.orig_stream.flush()


class LogsTab(QWidget):
    """Shows all app print() output and errors live."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # Keep original streams (so we can still see them in terminal)
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr

        # Redirect both to this text box
        sys.stdout = EmittingStream(self.text_edit, self._orig_stdout, show_time=True)
        sys.stderr = EmittingStream(self.text_edit, self._orig_stderr, show_time=True)