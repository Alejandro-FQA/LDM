from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_socketio import SocketIO, emit
from datetime import datetime
import threading

import socket
import signal
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'divulgacion_2025'

socketio = SocketIO(app, cors_allowed_origins="*", allow_headers=['Content-Type'], async_mode='threading')

# Global variable to control server shutdown
shutdown_flag = threading.Event()

# Store messages in memory (in production, use a database)
messages = []

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    origin = request.headers.get('Origin')
    if origin:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@app.route('/')
def index():
    return redirect(url_for('results_av'))

@app.route('/results_av')
def results_av():
    """Results page showing all messages"""
    return render_template('results_final_av_cat.html')

@app.route('/results_aa')
def results_aa():
    """Results page showing all messages"""
    return render_template('results_final_aa_cat.html')

@app.route('/results_estable')
def results_estable():
    """Results page showing binding energy stability"""
    return render_template('results_final_estable_cat.html')

@app.route('/download')
def download():
    """
    This can be used to download the .exe file
    """
    return send_file('interactive_plot2',as_attachment=True)

group_counter = 0
groups = {}
lock = threading.Lock()

@app.route("/create_group", methods=["POST", 'HEAD'])
def create_group():
    if request.method == 'HEAD':
        return 'OK', 200
    data = request.get_json()
    print(data)
    global group_counter
    with lock:
        try: 
            # If group is created, return group
            value = groups[data.get('ID')]
            return jsonify({"group_id": value})
        except:
            # Create group if not
            group_counter += 1
            group_id = data.get('ID')
            groups[group_id] = f'{group_counter}'
            return jsonify({"group_id": f'{group_counter}'})

received_results = {}
messages = []

def create_messages():
    # Create the messages
    global messages
    complete_data = []
    for key in list(received_results.keys())[1:]:
        for elem in list(received_results.get(key)):
            aA = received_results.get(key).get(elem).get('params').get('a_a',0)
            aV = received_results.get(key).get(elem).get('params').get('a_v',0)
            aminaa = received_results.get(key).get(elem).get('ranges').get('A_min_a_a',0)
            amaxaa = received_results.get(key).get(elem).get('ranges').get('A_max_a_a',0)
            aminav = received_results.get(key).get(elem).get('ranges').get('A_min_a_v',0)
            amaxav = received_results.get(key).get(elem).get('ranges').get('A_max_a_v',0)
            group_id = groups[key]
            element = elem
            
            # Get username from session (not implemented)
            username = session.get('username', 'Anonymous')
                        
            print(f"Received message from user: {username}")

            if group_id:
                message_data = {
                    #'text': message,
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
                complete_data.append(message_data)
                
    # Emit the new message to all connected clients
    print(f"Emitting message to all clients: {complete_data}")
    messages = complete_data
    socketio.emit('new_data', complete_data, namespace='/')
    print(f"Message `emitted successfully")

@app.route('/send', methods=['POST', 'OPTIONS', 'HEAD'])
def send_message():
    """Handle message submission"""
    if request.method == 'HEAD':
        return 'OK', 200 
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.get_json()
    group_id = str(data.get('ID'))
    keys = list(data.get(group_id).keys())
    params = data.get(group_id).get(keys[-1])
    print(params)

    # Only send the last received element, not ideal...
    aA = params.get('params').get('a_a',0)
    aV = params.get('params').get('a_v',0)
    aminaa = params.get('ranges',{0:0}).get('A_min_a_a',0)
    amaxaa = params.get('ranges',{0:0}).get('A_max_a_a',0)
    aminav = params.get('ranges',{0:0}).get('A_min_a_v',0)
    amaxav = params.get('ranges',{0:0}).get('A_max_a_v',0)
    group_id = groups[group_id]#data.get('group_id',0)
    element = keys[-1]#data.get('element','O')

    # Get username from session (set from cookies)
    username = session.get('username', 'Anonymous')
    
    # Also try to get username from cookie directly (for cross-origin requests from Jupyter)
    if not username or username == 'Anonymous':
        username = request.cookies.get('username', 'Anonymous')
    
    print(f"Received message from user: {username}")

    if group_id:
        message_data = {
            #'text': message,
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
        
        # Emit the new message to all connected clients
        print(f"Emitting message to all clients: {message_data}")
        socketio.emit('new_message', message_data, namespace='/')
        print(f"Message emitted successfully")
        
    received_results.update(data)
    print('results')
    print(received_results)
    create_messages()
    return '', 200

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """API endpoint to get all messages"""
    return jsonify({'messages': messages})

# Global shutdown control
shutdown_requested = False
server_thread = None

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Signal the server to shutdown gracefully"""
    global shutdown_requested
    
    print("Shutdown requested via endpoint")
    shutdown_requested = True
    
    # We need a more graceful shutdown
    def delayed_exit():
        import time
        time.sleep(1)  # Give time for response to be sent
        print("Performing clean shutdown...")
        # Use os._exit for clean exit from thread
        import os
        os._exit(0)
    
    # Start exit in background thread
    threading.Thread(target=delayed_exit, daemon=True).start()
    
    return jsonify({'message': 'Server shutting down gracefully...'}), 200

def run_server():
    """Run the Flask server"""
    # Get local IP address for display
    local_ip = get_local_ip()
    print(f"Starting server on 0.0.0.0:5001")
    print(f"Local access: http://localhost:5001")
    print(f"LAN access: http://{local_ip}:5001")
    print(f"Note: For internet access, configure port forwarding on your router")
    
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, use_reloader=False)

def get_local_ip():
    """Get local IP address"""
    try:
        # Create a dummy socket to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    run_server()
        