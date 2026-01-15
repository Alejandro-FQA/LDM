import sys
import json
import os
import requests

"""
Handles user configuration storage and retrieval using a JSON file, 
with support for PyInstaller bundles and Windows file hiding.
Provides functions to read/write user information and manage 
application-specific configuration data.
"""

def resource_path(relative_path):
    """Get absolute path to resource (handles PyInstaller bundles)."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_app_directory():
    """Get the directory where the executable or script resides (for writing)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_user_info_path():
    """Return full path to writable .user_info file."""
    return os.path.join(get_app_directory(), ".user_info")

def hide_file_windows(path):
    """Hide file on Windows."""
    if os.name == "nt":
        subprocess.run(["attrib", "+h", path], check=False)

def ensure_user_info_file(user_id):
    """
    Ensure .user_info exists and contains at least {"user_id": user_id}.
    """
    path = get_user_info_path()
    data = {}

    # If file exists, try loading JSON
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    # Ensure at least user_id
    if "ID" not in data:
        data["ID"] = user_id
    else:
        user_id = data["ID"]

    # Save JSON file (create or update)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Hide on Windows if new
    if not os.path.exists(path):
        hide_file_windows(path)

    return user_id

def read_user_info():
    path = get_user_info_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def connect2server(user_id, url):

    path = get_user_info_path()
    data = read_user_info()

    user_id = str(user_id)
    data["url"] = url

    print('URL saved')

    # Save JSON back to file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    url_group = f'{url}/create_group'
    group = None

    try:
        # Optional: quick check before sending
        response = requests.head(url_group, timeout=3)
        if response.status_code >= 400:
            print(f"Server reachable but returned {response.status_code}")
            return None

        # Now try to post the data
        response = requests.post(url_group, json={"ID": str(user_id)}, timeout=5)
        response.raise_for_status()  # Raise error for 4xx/5xx responses
        group = int(response.json().get('group_id'))
        print("Data successfully sent to server.")
        return group

    except requests.ConnectionError:
        print("Error: Could not connect to server.")
    except requests.Timeout:
        print("Error: Server timed out.")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error creating group: {e}")
        group = None

    return group  

def save_user_data(self):
    """Save current element parameters under this user ID in .user_info."""
    path = get_user_info_path()
    data = read_user_info()

    element = self.state.element.symbol
    user_id = str(self.state.id)
    last = 'last'

    # Ensure element key exists
    if element not in data:
        data[element] = {}
    # Ensure last key exists
    if last not in data:
        data[last] = {}

    # Indicate last saved element
    data[last] = element

    # Ensure sub-dictionaries exist
    data[element].setdefault("params", {})
    data[element].setdefault("ranges", {})

    

    # Tab 1 → save base parameters
    if self.state.current_tab.__class__.__name__ == "LDMTab":
        data[element]["params"].update({
            "a_v": self.state.params["a_v"],
            "a_s": self.state.params["a_s"],
            "a_c": self.state.params["a_c"],
            "a_a": self.state.params["a_a"],
            "a_p": self.state.params["a_p"],
        })
        print('Parameters saved successfully.')

    # Tab 2 → save range information
    elif self.state.current_tab.__class__.__name__ == "activity2_tab":
        if self.activity_index == 1:
            data[element]["ranges"].update({
                "A_min_a_a": self.adjust_spinbox['min'].value(),
                "A_max_a_a": self.adjust_spinbox['max'].value()
            })
            print('Asymmetry range saved successfully.')
        elif self.activity_index == 2:
            data[element]["ranges"].update({
                "A_min_a_v": self.adjust_spinbox['min'].value(),
                "A_max_a_v": self.adjust_spinbox['max'].value()
            })
            print('Volume range saved successfully.')

    # Save JSON back to file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print(f'{element} data saved successfully.')

def load_url(id):
    """Load saved URL for this user ID, if available."""
    path = get_user_info_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return None
        
    return data['url'] if 'url' in data else None

def load_user_params(state):
    """Load saved parameters for this user ID and current element, if available."""
    path = get_user_info_path()
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return None

    element = state.element.symbol
    user_data = data.get(element)

    print(f'{element} data loaded successfully.')

    return user_data

def send2server(url):
    url_send = f'{url}/send'
    data = read_user_info()

    try:
        # Optional: quick check before sending
        response = requests.head(url_send, timeout=3)
        print(f'response: {response}')
        if response.status_code >= 400:
            print(f"Server reachable but returned {response.status_code}")
            return False

        # Now try to post the data
        response = requests.post(url_send, json=data, timeout=5)
        response.raise_for_status()  # Raise error for 4xx/5xx responses
        print("Data successfully sent to server.")
        return True

    except requests.ConnectionError:
        print("Error: Could not connect to server.")
    except requests.Timeout:
        print("Error: Server timed out.")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    return False
    
def anyData(state):
    """
    Check whether the current element (state.element.symbol)
    has any saved parameters in the user's data file.
    """
    user_data = load_user_params(state)
    if user_data == None:
        return False    
    
    user_id = str(state.id)
    symbol = getattr(state.element, "symbol", None)

    if not symbol or user_id not in user_data:
        return False
    
    # Get the sub-dictionary for this element
    element_data = user_data[user_id].get(symbol, {})

    # Return True only if the element has parameters
    return bool(isinstance(element_data, dict) and element_data)
