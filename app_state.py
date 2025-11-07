# app_state.py
from PyQt5.QtCore import QObject, pyqtSignal

import numpy as np

import user_config as uc
from element import Element
from read_data import AtomicMassData


class AppState(QObject):        
    """ Contains shared information among tabs."""

    # signals to notify all tabs
    parameterChanged = pyqtSignal(str, object)
    languageChanged = pyqtSignal(str)
    elementChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Get Atomic Mass Data
        data_file = uc.resource_path("atomic_mass.txt")
        self.data = AtomicMassData(data_file)

        # User inteface
        self.language = "CAT"
        self.id = uc.ensure_user_info_file(np.random.randint(10**5))
        self.group = uc.connect2server(self.id)

        # Default activity
        self.current_tab = 0

        # Default element
        self.element = Element('O', self.data, self.language)

        # Default parameters
        self.default_params = {
            "a_v": 15.8,
            "a_s": 18.3,
            "a_c": 0.714,
            "a_a": 23.2,
            "a_p": 12.0,
        }
        # Optimized parameters
        self.params = self.default_params.copy()

    # -----------------------------
    # Update functions
    # -----------------------------
    def set_param(self, key, value):        
        self.params[key] = value
        self.parameterChanged.emit(key, value)

    def set_language(self, lang):
        self.language = lang
        self.languageChanged.emit(lang)

    def set_element(self, element_label):
        element = element_label.split()[0]
        self.element = Element(element, self.data, self.language)
        self.elementChanged.emit()

   