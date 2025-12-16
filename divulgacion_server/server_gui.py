import sys
import threading
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QGroupBox, QLineEdit)
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
import socket
from datetime import datetime

import functools
from flask import request

# Import your Flask app
try:
    from server import app, socketio, messages
except ImportError:
    print("Warning: Could not import server module. Using mock for testing.")
    # Mock objects for testing
    class MockApp:
        def run(self, host, port, debug):
            print(f"Mock server running on {host}:{port}")
    
    class MockSocketIO:
        def run(self, *args, **kwargs):
            pass
    
    app = MockApp()
    socketio = MockSocketIO()
    messages = []

class ServerThread(QObject):
    """Worker thread to run Flask server without blocking GUI"""
    server_started = pyqtSignal(str)
    server_stopped = pyqtSignal()
    log_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.thread = None
        self.should_stop = False
        
    def run_server(self, host='0.0.0.0', port=5001):
        """Run the Flask server in a separate thread"""
        # Reset stop flag for new start
        self.should_stop = False
        
        try:
            self.running = True
            server_url = f"http://{host}:{port}"
            self.server_started.emit(server_url)
            self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Starting server on {server_url}")
            
            # Import and run the server function
            from server import run_server
            run_server()
            
        except SystemExit:
            # This is expected when server shuts down via os._exit()
            self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Server shut down cleanly")
        except Exception as e:
            self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {str(e)}")
        finally:
            self.running = False
            self.server_stopped.emit()
            
    def stop_server(self):
        """Stop the server via shutdown endpoint"""
        if not self.running:
            return
            
        try:
            # Make a request to the shutdown endpoint
            import requests
            self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Sending shutdown request...")
            
            # Try to send shutdown request
            try:
                response = requests.post('http://localhost:5001/shutdown', timeout=2)
                self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Shutdown response: {response.status_code}")
            except requests.exceptions.ConnectionError:
                # Server might already be down
                self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Server appears to be stopped")
            except Exception as e:
                self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {str(e)}")
                
            # Set flag to prevent restart issues
            self.should_stop = True
            
        except Exception as e:
            self.log_message.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Error in stop_server: {str(e)}")

class ServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server_thread = None
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Flask Server Controller')
        self.setGeometry(100, 100, 900, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Server Control Section
        control_group = QGroupBox("Server Control")
        control_layout = QVBoxLayout()
        
        # URL display
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Server URL:"))
        self.url_label = QLabel("Server not started")
        url_layout.addWidget(self.url_label)
        url_layout.addStretch()
        
        # Copy URL button
        self.copy_url_btn = QPushButton("Copy URL")
        self.copy_url_btn.clicked.connect(self.copy_url)
        url_layout.addWidget(self.copy_url_btn)
        
        # Open in browser button
        self.open_browser_btn = QPushButton("Open in Browser")
        self.open_browser_btn.clicked.connect(self.open_in_browser)
        url_layout.addWidget(self.open_browser_btn)
        
        control_layout.addLayout(url_layout)
        
        # Server buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Server")
        self.start_btn.clicked.connect(self.start_server)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Server")
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        control_layout.addLayout(button_layout)
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

                # Log Display Section
        log_group = QGroupBox("Server Log")
        log_layout = QVBoxLayout()
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(150)
        log_layout.addWidget(self.log_display)
        
        # Clear log button
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(clear_log_btn)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # Messages Display Section
        messages_group = QGroupBox("Received Messages")
        messages_layout = QVBoxLayout()
        
        self.messages_display = QTextEdit()
        self.messages_display.setReadOnly(True)
        messages_layout.addWidget(self.messages_display)
        
        # Refresh messages button
        refresh_btn = QPushButton("Refresh Messages")
        refresh_btn.clicked.connect(self.refresh_messages)
        messages_layout.addWidget(refresh_btn)
        
        messages_group.setLayout(messages_layout)
        main_layout.addWidget(messages_group)
        
        # Auto-refresh timer for messages
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_messages)
        self.refresh_timer.start(2000)  # Refresh every 2 seconds
        
        # Status bar
        self.statusBar().showMessage('Ready')

    def start_server(self):
        """Start the Flask server in a separate thread"""
        # Ensure any previous thread is cleaned up
        self.cleanup_previous_server()
        
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] Starting server...")
        
        # Create new worker and thread
        self.worker = ServerThread()
        self.server_thread = threading.Thread(
            target=self.worker.run_server,
            daemon=True
        )
        
        # Connect signals
        self.worker.server_started.connect(self.on_server_started)
        self.worker.server_stopped.connect(self.on_server_stopped)
        self.worker.log_message.connect(self.log_message)
        
        # Start the thread
        self.server_thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.statusBar().showMessage('Server starting...')

    def cleanup_previous_server(self):
        """Clean up any previous server thread"""
        if hasattr(self, 'worker') and self.worker:
            if self.worker.running:
                self.worker.stop_server()
            # Give it a moment to clean up
            import time
            time.sleep(0.5)
            
    def on_server_stopped(self):
        """Handle server stopped signal"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.url_label.setText("Server not started")
        self.statusBar().showMessage('Server stopped')
        
    def stop_server(self):
        """Stop the Flask server"""
        if self.worker and self.worker.running:
            self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] Stopping server...")
            self.worker.stop_server()

    def stop_server(self):
        """Stop the Flask server"""
        if self.worker and self.worker.running:
            self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] Stopping server...")
            self.worker.stop_server()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.statusBar().showMessage('Server stopping...')
        
    def on_server_started(self, url):
        """Handle server started signal"""
        # Get local IP for better display
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            display_url = f"http://{local_ip}:5001 (LAN)"
        except:
            display_url = url
            
        self.url_label.setText(display_url)
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] Server started successfully")
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] Local URL: {url}")
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] LAN URL: http://{local_ip if 'local_ip' in locals() else 'YOUR_LOCAL_IP'}:5001")
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] For internet access:")
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] 1. Configure port forwarding on your router")
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] 2. Forward port 5001 to your local IP")
        self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] 3. Use your public IP (find at: https://whatismyipaddress.com/)")
        self.statusBar().showMessage(f'Server running on {display_url}')
    
    def log_message(self, message):
        """Add a message to the log display"""
        self.log_display.append(message)
        self.log_display.verticalScrollBar().setValue(
            self.log_display.verticalScrollBar().maximum()
        )
        
    def refresh_messages(self):
        """Refresh the messages display from the server module"""
        try:
            from server import messages  # Import fresh each time
            
            self.messages_display.clear()
            if not messages:
                self.messages_display.append("No messages received yet")
                return
                
            for msg in messages:
                display_text = f"""
                [{msg.get('timestamp', 'N/A')}] Group {msg.get('group_id', 'N/A')} - Element: {msg.get('element', 'N/A')}
                aA: {msg.get('aA', 0)}, aV: {msg.get('aV', 0)}
                Ranges: A_min_a_a={msg.get('A_min_a_a', 0)}, A_max_a_a={msg.get('A_max_a_a', 0)}
                       A_min_a_v={msg.get('A_min_a_v', 0)}, A_max_a_v={msg.get('A_max_a_v', 0)}
                Username: {msg.get('username', 'Anonymous')}
                {'-' * 60}
                """
                self.messages_display.append(display_text)
                
            self.messages_display.verticalScrollBar().setValue(
                self.messages_display.verticalScrollBar().maximum()
            )
            
        except ImportError as e:
            self.messages_display.append(f"Error importing messages: {str(e)}")
        except Exception as e:
            self.messages_display.append(f"Error refreshing messages: {str(e)}")
    
    def get_local_ip(self):
        """Get the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "localhost"

    def copy_url(self):
        """Copy server URL to clipboard"""
        url = f'http://{self.get_local_ip()}'
        if url != "Server not started":
            clipboard = QApplication.clipboard()
            clipboard.setText(url)
            self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] URL copied to clipboard")
                    
    def open_in_browser(self):
        """Open server URL in default browser"""
        url = f'http://{self.get_local_ip()}:5001'
        if url != "Server not started":
            webbrowser.open(url)
            self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] Opening {url} in browser")
    
    def clear_log(self):
        """Clear the log display"""
        self.log_display.clear()
        
    def closeEvent(self, event):
        """Handle window close event"""
        if self.worker and self.worker.running:
            self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] WARNING: Server is still running!")
            self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] The server will continue running in background")
        
        self.refresh_timer.stop()
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = ServerGUI()
    window.show()
    
    # Start server automatically if desired (uncomment next line)
    # QTimer.singleShot(1000, window.start_server)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()   