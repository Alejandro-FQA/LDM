import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

class SharedParams(QObject):
    changed = pyqtSignal(str, object)  # emits (key, new_value)

    def __init__(self):
        super().__init__()

        

    
            
        