import os
import sys
import socket
import threading
import signal
from datetime import datetime

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_socketio import SocketIO, emit


def create_app():
    # Determine the correct template folder depending on frozen or normal run
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle: templates are extracted to sys._MEIPASS/divulgacion_server/templates
        template_folder = os.path.join(sys._MEIPASS, 'divulgacion_server', 'templates')
    else:
        # Development: relative to this file (server.py)
        template_folder = os.path.join(os.path.dirname(__file__), 'templates')

    app = Flask(__name__, template_folder=template_folder)
    app.config['SECRET_KEY'] = 'divulgacion_2025'

    return app


# Create the Flask app
app = create_app()

# Initialize SocketIO with threading mode (most reliable with PyInstaller)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables
shutdown_flag = threading.Event()
messages = []
received_results = {}
groups = {}
group_counter = 0
lock = threading.Lock()
shutdown_requested = False
server_thread = None


# CORS headers for all responses
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response


# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")


@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")


# Routes
@app.route('/')
def index():
    return redirect(url_for('results_av'))


@app.route('/results_av')
def results_av():
    return render_template('results_final_av_cat.html')


@app.route('/results_aa')
def results_aa():
    return render_template('results_final_aa_cat.html')


@app.route('/results_estable')
def results_estable():
    return render_template('results_final_estable_cat.html')


@app.route('/download')
def download():
    """
    This can be used to download the .exe file (or any other file)
    Adjust the path if needed.
    """
    # Example: sending a file that is bundled as data
    if getattr(sys, 'frozen', False):
        file_path = os.path.join(sys._MEIPASS, 'interactive_plot2')
    else:
        file_path = os.path.join(os.path.dirname(__file__), 'interactive_plot2')

    return send_file(file_path, as_attachment=True)


@app.route("/create_group", methods=["POST", "HEAD"])
def create_group():
    if request.method == 'HEAD':
        return 'OK', 200

    data = request.get_json()
    client_id = data.get('ID')

    with lock:
        if client_id in groups:
            return jsonify({"group_id": groups[client_id]})
        else:
            global group_counter
            group_counter += 1
            groups[client_id] = str(group_counter)
            return jsonify({"group_id": str(group_counter)})


def create_messages():
    """Rebuild the complete messages list from received_results"""
    global messages
    complete_data = []

    # get keys
    user_id = received_results.get('ID')
    elements = [k for k in received_results.keys() if k not in {'ID', 'url', 'last'}]

    for element in elements:
        item = received_results[element]
        message_data = {
            'username': session.get('username', 'Anonymous'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'aA': item.get('params', {}).get('a_a', 0),
            'aV': item.get('params', {}).get('a_v', 0),
            'element': element,
            'group_id': groups.get(str(user_id), '0'),
            'A_min_a_a': item.get('ranges', {}).get('A_min_a_a', 0),
            'A_max_a_a': item.get('ranges', {}).get('A_max_a_a', 0),
            'A_min_a_v': item.get('ranges', {}).get('A_min_a_v', 0),
            'A_max_a_v': item.get('ranges', {}).get('A_max_a_v', 0),
        }
        complete_data.append(message_data)

    messages = complete_data
    socketio.emit('new_data', complete_data)


@app.route('/send', methods=['POST', 'OPTIONS', 'HEAD'])
def send_message():
    if request.method == 'HEAD':
        return 'OK', 200
    if request.method == 'OPTIONS':
        return '', 204

    # retireve data
    data = request.get_json()
    user_id = data['ID']
    element = data['last']
    data_element = data[element]

    # Extract values
    params = data_element.get('params', {})
    aA = params.get('a_a', 0)
    aV = params.get('a_v', 0)

    ranges = data_element.get('ranges', {})
    aminaa = ranges.get('A_min_a_a', 0)
    amaxaa = ranges.get('A_max_a_a', 0)
    aminav = ranges.get('A_min_a_v', 0)
    amaxav = ranges.get('A_max_a_v', 0)
    group_id = groups.get(str(user_id), '0')

    username = session.get('username', 'Anonymous')
    if username == 'Anonymous':
        username = request.cookies.get('username', 'Anonymous')

    message_data = {
        'username': username,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'aA': aA,
        'aV': aV,
        'element': element,
        'group_id': group_id,
        'A_min_a_a': aminaa,
        'A_max_a_a': amaxaa,
        'A_min_a_v': aminav,
        'A_max_a_v': amaxav,
    }

    messages.append(message_data)
    socketio.emit('new_message', message_data)

    # Update global results and rebuild complete list
    received_results.update(data)
    create_messages()

    return '', 200


@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})


@app.route('/shutdown', methods=['POST'])
def shutdown():
    global shutdown_requested
    print("Shutdown requested via endpoint")
    shutdown_requested = True

    def delayed_exit():
        import time
        time.sleep(1)
        print("Performing clean shutdown...")
        os._exit(0)

    threading.Thread(target=delayed_exit, daemon=True).start()
    return jsonify({'message': 'Server shutting down gracefully...'}), 200


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def run_server():
    local_ip = get_local_ip()
    print(f"Starting server on 0.0.0.0:5001")
    print(f"Local access: http://localhost:5001")
    print(f"LAN access: http://{local_ip}:5001")
    print(f"Note: For internet access, configure port forwarding on your router")

    socketio.run(app, host='0.0.0.0', port=5001, debug=False, use_reloader=False)


if __name__ == '__main__':
    run_server()