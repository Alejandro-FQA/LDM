import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel, QLineEdit
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor


from app_state import AppState
from user_config import connect2server, load_url


class StatusIndicator(QLabel):
    """Simple circular status indicator (red/green)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)  # Fixed size for the circle
        self._connected = False
    
    def set_connected(self, connected):
        self._connected = connected
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw circle
        if self._connected:
            color = QColor(0, 255, 0)  # Green when connected
        else:
            color = QColor(255, 0, 0)  # Red when disconnected
        
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())


class EmittingStream:
    """(Keep your existing EmittingStream class unchanged)"""
    def __init__(self, text_edit, orig_stream=None, show_time=True):
        self.text_edit = text_edit
        self.orig_stream = orig_stream
        self.show_time = show_time

    def write(self, text):
        text = text.strip()
        if text:
            timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] " if self.show_time else ""
            formatted_text = f"{timestamp}{text}"
            QTimer.singleShot(0, lambda: self.text_edit.append(formatted_text))
        if self.orig_stream:
            self.orig_stream.write(text + "\n")
            self.orig_stream.flush()

    def flush(self):
        if self.orig_stream:
            self.orig_stream.flush()


class LogsTab(QWidget):
    """Shows all app print() output and errors live."""
    def __init__(self, app_state: AppState):
        super().__init__()
        
        # App_state info
        self.state = app_state

        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create control panel (horizontal layout for server controls)
        control_layout = QHBoxLayout()
        
        # Server label
        server_label = QLabel("Server:")
        control_layout.addWidget(server_label)
        
        # Server URL input field
        self.server_input = QLineEdit()
        self.state.server_url  = load_url(self.state.id)
        if not self.state.server_url:
            self.server_input.setPlaceholderText("Enter server URL (e.g., http://localhost:8080)")
        else:
            self.server_input.setText(self.state.server_url)
        self.server_input.setMinimumWidth(300)  # Make it reasonably wide
        control_layout.addWidget(self.server_input)
        
        # Connect button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.on_connect_clicked)
        control_layout.addWidget(self.connect_btn)
        
        # Status indicator
        self.status_indicator = StatusIndicator()
        control_layout.addWidget(self.status_indicator)
        
        # Add stretch to push everything to the left
        control_layout.addStretch()
        
        # Add control panel to main layout
        main_layout.addLayout(control_layout)
        
        # Text edit for logs
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        main_layout.addWidget(self.text_edit)

        # Keep original streams
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr

        # Redirect both to this text box
        sys.stdout = EmittingStream(self.text_edit, self._orig_stdout, show_time=True)
        sys.stderr = EmittingStream(self.text_edit, self._orig_stderr, show_time=True)
        
        # Initialize connection state
        self.is_connected = False
    
    def on_connect_clicked(self):
        """Slot for connect button click."""
        self.state.server_url = self.server_input.text().strip()
        if not self.state.server_url:
            print("Error: Please enter a server URL")
            return        
    
        # Toggle connection state for demonstration
        # In your real implementation, you'll connect to the actual server
        self.state.group = connect2server(user_id=self.state.id, url=self.state.server_url)
        self.is_connected = self.state.group is not None
        self.status_indicator.set_connected(self.is_connected)
        
        if self.is_connected:
            self.connect_btn.setText("Connected")
            self.connect_btn.setEnabled(False)
            print(f"Connected to server: {self.state.server_url}")
            print(f"Assigned to group: {self.state.group}")
        else:
            self.connect_btn.setText("Connect")
            print(f"Disconnected from server: {self.state.server_url}")