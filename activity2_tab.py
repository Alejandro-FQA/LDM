import sys
import os
import json
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QLabel, QTabWidget, QTextEdit, QPushButton, QComboBox, QToolBox,
    QCheckBox, QTextBrowser, QFrame, QSplitter, QSpinBox, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from scipy.signal import argrelmin

import requests
import subprocess
import importlib


# Custom imports
from app_state import AppState
from elements_diccionaries import elements_label as els_lab
# import activity2_cat
import user_config as uc
from ldm_model import ldm_model
from element import Element

def load_activity_module(language: str, activity_number: int):
    module_path = f"activities.{language}.activity{activity_number}_{language}"
    module = importlib.import_module(module_path)
    return module

# -----------------------------
# Tab 2: Heaviest isotopes
# -----------------------------
class activity2_tab(QWidget):
    def __init__(self, app_state: AppState):
        super().__init__()
        
        # Tab state
        self.active = False
        
        # App State
        self.state = app_state
        self.state.parameterChanged.connect(self.on_param_changed)
        self.state.languageChanged.connect(self.on_language_changed)
        self.state.elementChanged.connect(self.on_element_changed)

        # Activity sections
        self.sections = [
            ("intro", "Introducció"),
            ("section1", "Activitat 2a - Incertesa del Paràmetre d'Asimetria"),
            ("section2", "Activitat 2b - Incertesa del Paràmetre de Volum")
        ]

        # Default activity
        self.activity_mod = load_activity_module(self.state.language, 2)
        self.activity_index = 0
        self.activity_text = {}

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # ----------------- Left column ----------------
        left_widget = QWidget()
        left_widget.setMinimumWidth(400)
        left_layout = QVBoxLayout(left_widget)

        # ----------------- Element buttons -----------------        
        element_layout = QHBoxLayout()
        self.label1 = QLabel()
        element_layout.addWidget(self.label1, stretch=1)
        self.elements_box = QComboBox()
        element_layout.addWidget(self.elements_box, stretch=10)
        self.language_box = QComboBox()
        element_layout.addWidget(self.language_box, stretch=1)        

        # Fill the list of elements
        self.languages_list = ["CAT", "ES", "EN"]
        self.language_box.addItems(self.languages_list)
        # Select default element and update it
        self.language_box.setCurrentIndex(self.languages_list.index(self.state.language))

        # Create list of elements  
        self.language_box.setMaxVisibleItems(10)  # Show max 10 items at once
        self.language_box.setStyleSheet("QComboBox { combobox-popup: 0; }")  # Force maxVisibleItems to work
             
        self.elements_box.setMaxVisibleItems(10)  # Show max 10 items at once
        self.elements_box.setStyleSheet("QComboBox { combobox-popup: 0; }")  # Force maxVisibleItems to work
        
        # Connect list signals to slots
        self.language_box.currentTextChanged.connect(self.state.set_language)
        self.elements_box.currentTextChanged.connect(self.state.set_element) 

        # Update data
        left_layout.addLayout(element_layout) 

        # ----------------- Plots area -----------------
        # Matplotlib figure 
        self.figure = Figure(figsize=(7, 6), constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        left_layout.addWidget(self.canvas, stretch=4)

        # --- Connect mouse events ---
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

        # State for dragging
        self._is_dragging = False
        self._last_mouse_pos = None
        self._active_ax = None  

        self.ax1 = self.figure.add_subplot(111)
        
        # -------------- Adjust Boxes ----------------
        adjust_layout = QHBoxLayout()

        self.adjust_spinbox = {}
        self.adjust_set_button = {}
        self.adjust_label = {}

        # Find the zeros of the binding energy
        A_model = np.arange(1000) + 1
        B_model = ldm_model(self.state.element, self.state.params, A_model)
        idx_zeros = argrelmin(np.abs(B_model), order=10)[0]
        if B_model[idx_zeros[-1]] < 0:
            idx_max = idx_zeros[-1] - 1
        else:
            idx_max = idx_zeros[-1]

        for key in ['min', 'max']:
            pair_layout = QHBoxLayout()

            label = QLabel(f"<html>A<sub>{key}</sub> =</html>")
            label.setFixedWidth(65)

            spinbox = QSpinBox()
            spinbox.setFixedWidth(65)
            spinbox.setRange(0, 1000)
            spinbox.setSingleStep(1)            
            spinbox.setValue(A_model[idx_max])
            spinbox.valueChanged.connect(self.on_adjust_spinbox_changed)
            spinbox.setEnabled(False)

            button = QPushButton('Fixa')
            button.setFixedWidth(65)
            button.clicked.connect(lambda _, k=key: self.on_set_button_clicked(k))
            button.setEnabled(False)
                        
            pair_layout.addWidget(label)
            pair_layout.addWidget(spinbox)
            pair_layout.addWidget(button)
            pair_layout.setSpacing(1)

            adjust_layout.addLayout(pair_layout)
            self.adjust_spinbox[key] = spinbox    
            self.adjust_set_button[key] = button
            self.adjust_label[key] = label
        
        adjust_layout.setSpacing(20)
        left_layout.addLayout(adjust_layout)


        # ----------------- Sliders area -----------------
        sliders_title = QLabel("Paràmetres del Model de la Gota Líquida (MeV)")
        sliders_title.setAlignment(Qt.AlignCenter) 
        sliders_layout = QVBoxLayout()
        left_layout.addWidget(sliders_title)
        left_layout.addLayout(sliders_layout, stretch=1)

        # Define parameter-specific ranges and scaling
        param_ranges = {
            "a_v": (0, 30),    # MeV
            "a_s": (0, 30),
            "a_c": (0, 2),
            "a_a": (0, 50),
            "a_p": (0, 30)
        }
        
        self.scale = 100 # slider steps per unit

        self.params_slider = {}
        self.params_label = {}
        self.params_spinbox = {}
        self.params_checker = {}

        for key, value in self.state.params.items():
            slider_layout = QHBoxLayout()
            pretty_name = { 
                "a_v": "<li><i>a<sub>v</sub></i>",
                "a_s": "<li><i>a<sub>s</sub></i>",
                "a_c": "<li><i>a<sub>c</sub></i>",
                "a_a": "<li><i>a<sub>a</sub></i>",
                "a_p": "<li><i>a<sub>p</sub></i>"
            }[key]

            label = QLabel(f"<html>{pretty_name} =</html>")
            spinbox = QDoubleSpinBox()
            slider = QSlider(Qt.Horizontal)
            checker = QCheckBox()
            
            # Apply parameter-specific limits
            min_val, max_val = param_ranges[key]
            slider.setMinimum(int(min_val * self.scale))
            slider.setMaximum(int(max_val * self.scale))
            slider.setValue(int(value * self.scale))
            slider.valueChanged.connect(lambda v, k=key: self.state.set_param(k, v/self.scale))

            spinbox.setFixedWidth(65)
            spinbox.setRange(min_val, max_val)
            spinbox.setSingleStep(0.01)
            spinbox.setDecimals(2)
            spinbox.setValue(value)
            spinbox.valueChanged.connect(lambda v, k=key: self.state.set_param(k, v))

                
            # Check sliders
            checker.setChecked(True)
            checker.toggled.connect(slider.setEnabled)
            checker.toggled.connect(spinbox.setEnabled)

            slider_layout.addWidget(label)
            slider_layout.addWidget(spinbox)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(checker)
            sliders_layout.addLayout(slider_layout)
            
            self.params_slider[key] = slider
            self.params_label[key] = label
            self.params_spinbox[key] = spinbox
            self.params_checker[key] = checker      

        # ----------------- Right column ----------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Title label with styling
        title_label = QLabel("Predicció dels Isòtops més pesats")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
            }
        """)

        right_layout.addWidget(title_label)

        # ----------------- Text area -----------------
        # Text box on the right with instructions

        num = 2
        activity = self.activity_mod.get_activity(self.state)
        self.toolbox = QToolBox()
                
        self.activity_index = self.toolbox.currentIndex()

        for section_key, title in self.sections:            
            text_browser = QTextBrowser()
            text_browser.setHtml(activity[section_key])
            text_browser.setOpenExternalLinks(True)
            self.activity_text[section_key] = text_browser
            self.toolbox.addItem(text_browser, title)

           
        right_layout.addWidget(self.toolbox)

        # ----------------- Buttons area -----------------
        button_layout = QHBoxLayout()
        
        # Create buttons
        self.reset_button = QPushButton("Reseteja")
        self.save_button = QPushButton("Desa")
        self.load_button = QPushButton("Carrega")
        self.send_button = QPushButton("Envia")
        self.info_button = QPushButton("ⓘ")      

        self.send_button.setEnabled(False) 
        self.save_button.setEnabled(False)
        
        # Connect button signals to slots
        self.reset_button.clicked.connect(self.reset_parameters)
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.load_button.clicked.connect(self.on_load_button_clicked)
        self.send_button.clicked.connect(self.on_send_button_clicked)
        self.info_button.clicked.connect(self.show_popup)

        # Connect signal
        self.toolbox.currentChanged.connect(self.on_activity_changed)

        # Add buttons to button layout
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.info_button)

        # Load button disabled
        self.update_load_button()
        
        # Add stretch to push buttons to the left (optional)
        button_layout.addStretch()

        right_layout.addLayout(button_layout)

        # ----------------- Add Layouts ----------------        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([500, 500])
        splitter.setStyleSheet("""
                QSplitter::handle {
                    background-color: #eee;   /* light grey line */
                    border: 1px solid #888;   /* optional outline */
                }
                QSplitter::handle:hover {
                    background-color: #ccc;   /* darker when hovered */
                }
            """)

        main_layout.addWidget(splitter)
        
        # Initial plot
        self.state.set_language(self.state.language)
        self.state.set_element('O')
        # self.reset_parameters()
        self.update_plots()
                
    # -----------------------------
    # Tab signal
    # ----------------------------- 
    def set_active(self, active: bool):
        self.active = active

        if active:
            for key, value in self.state.params.items():
                self.state.set_param(key, value)

    def show_popup(self):

        # Create a popup message box
        msg = QMessageBox(self)
        msg.setWindowTitle("-- Informació --")
        msg.setText(self.activity_mod.get_info())
        msg.setIcon(QMessageBox.Information)

        msg.exec_()  # This call blocks until the popup is closed


    # -----------------------------
    # On- functions
    # -----------------------------     
    def on_param_changed(self, key, value):
        """When parameter changes, update UI elements of visible tab"""
        if not self.isVisible():
            return
        # Update interactive elements
        self.update_slider(key, value)
        self.update_spinbox(key, value)
        self.update_plots()
        self.update_text()

    def on_language_changed(self, language):
        """When language changes, update UI texts."""
        # Update language
        self.update_language()
        # Update language box
        self.language_box.blockSignals(True)
        self.language_box.setCurrentIndex(self.languages_list.index(self.state.language))
        self.language_box.blockSignals(False)
        # Update label
        self.label1.setText(els_lab.get(language))
        # Update elements box
        self.update_elements_box()
        # Update text
        self.update_text()
    
    def on_element_changed(self):
        """When element changes, update UI plots and texts."""
        # Update 
        self.update_plots()
        self.update_elements_box()
        self.update_text()
        self.update_load_button()

    def on_save_button_clicked(self):
        """Save current parameters."""
        uc.save_user_data(self)
        # Update load button
        self.update_load_button()

    def on_load_button_clicked(self):
        """Try to load parameters, then update them.""" 
        user_data = uc.load_user_params(self.state)

        # --- Load base parameters ---
        new_params = user_data.get('params', {})
        for key, value in new_params.items():
            self.state.set_param(key, value)
        
        # --- Load ranges if they exist ---
        new_ranges = user_data.get('ranges', {})
        if new_ranges:  # Only if not empty
            if self.activity_index == 1:
                if 'A_min_a_a' in new_ranges:
                    self.adjust_spinbox['min'].setValue(new_ranges['A_min_a_a'])
                if 'A_max_a_a' in new_ranges:
                    self.adjust_spinbox['max'].setValue(new_ranges['A_max_a_a'])
            elif self.activity_index == 2:
                if 'A_min_a_v' in new_ranges:
                    self.adjust_spinbox['min'].setValue(new_ranges['A_min_a_v'])
                if 'A_max_a_v' in new_ranges:
                    self.adjust_spinbox['max'].setValue(new_ranges['A_max_a_v'])

    def safe_set(spinbox, value):
        if value is not None:
            spinbox.setValue(value)        

    def on_send_button_clicked(self):
        """Send parameters to server"""
        if self.state.is_connected:
            # Ensure user file exists
            uc.ensure_user_info_file(self.state.id)

            # Ensure there are some parameters of current element
            # otherwise, save current parameters
            if uc.anyData(self.state):
                uc.send2server(self.state.server_url)
            else:
                uc.save_user_data(self)
                self.update_load_button()
                uc.send2server(self.state.server_url)
        else:
            print("Please, connect to a server")

    def on_activity_changed(self, index):
        # Update plots
        self.activity_index = index
        self.update_plots()

        # Check out sliders
        # Enable buttons
        match index:
            case 0:            
                for key, checker in self.params_checker.items():
                    checker.setChecked(True)
                
                for key, spinbox in self.adjust_spinbox.items():
                    spinbox.setEnabled(False)
                for key, button in self.adjust_set_button.items():
                    button.setEnabled(False)

                for key, label in self.adjust_label.items():
                    label.setText(f"<html>A<sub>{key}</sub> =</html>")

                self.send_button.setEnabled(False)
                self.save_button.setEnabled(False)

            case 1:            
                for key, checker in self.params_checker.items():
                    if key not in ("a_a"):
                        checker.setChecked(False)
                    else:
                        checker.setChecked(True)

                for key, spinbox in self.adjust_spinbox.items():
                    spinbox.setEnabled(True)
                for key, button in self.adjust_set_button.items():
                    button.setEnabled(True)

                for key, label in self.adjust_label.items():
                    label.setText(f"<html>A<sub>{key}</sub><sup>(<i>aₐ</i>)</sup> =</html>")
                    
                self.send_button.setEnabled(True)
                self.save_button.setEnabled(True)

            case 2:            
                for key, checker in self.params_checker.items():
                    if key not in ("a_v"):
                        checker.setChecked(False)
                    else:
                        checker.setChecked(True)
                
                for key, spinbox in self.adjust_spinbox.items():
                    spinbox.setEnabled(True)
                for key, button in self.adjust_set_button.items():
                    button.setEnabled(True)

                for key, label in self.adjust_label.items():
                    label.setText(f"<html>A<sub>{key}</sub><sup>(<i>aᵥ</i>)</sup> =</html>")

                self.send_button.setEnabled(True)
                self.save_button.setEnabled(True)

    def on_adjust_spinbox_changed(self):
        A_min = self.adjust_spinbox['min'].value()
        A_max = self.adjust_spinbox['max'].value()
        
        # Ensure A_min <= A_max
        if A_min > A_max:
            # Determine which spinbox was changed by checking which one has focus
            # or use a different approach to track the source
            if self.adjust_spinbox['min'].hasFocus():
                # min was increased beyond max, so adjust max
                A_max = A_min
            else:
                # max was decreased below min, so adjust min
                A_min = A_max
        
        # Block signals to prevent recursive calls
        self.adjust_spinbox['min'].blockSignals(True)
        self.adjust_spinbox['max'].blockSignals(True)
        
        # Update values if they were changed
        if self.adjust_spinbox['min'].value() != A_min:
            self.adjust_spinbox['min'].setValue(A_min)
        if self.adjust_spinbox['max'].value() != A_max:
            self.adjust_spinbox['max'].setValue(A_max)
        
        self.adjust_spinbox['min'].blockSignals(False)
        self.adjust_spinbox['max'].blockSignals(False)
        
        self.update_plots()

    def on_set_button_clicked(self, key):
        # Find the zeros of the binding energy
        A_model = np.arange(1000) + 1
        B_model = ldm_model(self.state.element,
                            self.state.params,
                            A_model)
        idx_zeros = argrelmin(np.abs(B_model), order=10)[0]
        if B_model[idx_zeros[-1]] < 0:
            idx_max = idx_zeros[-1] - 1
        else:
            idx_max = idx_zeros[-1]

        # Set value in the box
        self.adjust_spinbox[key].setValue(A_model[idx_max])

    def on_scroll(self, event):
        """Zoom in/out when scrolling over a subplot."""
        if event.inaxes not in [self.ax1]:
            return

        ax = event.inaxes
        base_scale = 1.2

        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        xdata, ydata = event.xdata, event.ydata

        scale_factor = 1 / base_scale if event.button == "up" else base_scale

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])

        self.canvas.draw_idle()


    def on_press(self, event):
        """Start panning when left mouse button is pressed."""
        if event.inaxes not in [self.ax1]:
            return
        if event.button == 1:  # Left button
            self._is_dragging = True
            self._last_mouse_pos = (event.xdata, event.ydata)
            self._active_ax = event.inaxes


    def on_motion(self, event):
        """Handle dragging motion for panning."""
        if not self._is_dragging or event.inaxes != self._active_ax:
            return
        if event.xdata is None or event.ydata is None:
            return  # Ignore out-of-bounds drags

        ax = self._active_ax
        dx = event.xdata - self._last_mouse_pos[0]
        dy = event.ydata - self._last_mouse_pos[1]

        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()

        ax.set_xlim(cur_xlim[0] - dx, cur_xlim[1] - dx)
        ax.set_ylim(cur_ylim[0] - dy, cur_ylim[1] - dy)

        self.canvas.draw_idle()
        self._last_mouse_pos = (event.xdata, event.ydata)


    def on_release(self, event):
        """End panning when mouse is released."""
        self._is_dragging = False
        self._active_ax = None


    # -----------------------------
    # Update functions
    # ----------------------------- 
    def reset_parameters(self, default=False):
        """Reset parameters to default or 25% deviation"""  
        if default:
            self.state.params = self.state.default_params
        else:
            for key, value in self.state.default_params.items():
                if self.params_checker[key].isChecked():
                    random = (1 + 0.25 * (2 * np.random.rand() - 1))
                    self.state.set_param(key, value * random)

    def update_elements_box(self):
        # index = self.elements_box.currentIndex()
        index = self.state.element.Z
        # Replace all items in the combo box
        self.elements_box.blockSignals(True)
        self.elements_box.clear()
        # Get current language text (e.g. "CAT", "ES", "EN")
        self.elements_box.addItems(
            [el + f" (Z={i})" for i, el in  enumerate(self.state.data.list_elements(language=self.state.language))]
        )
        self.elements_box.setCurrentIndex(index)
        self.elements_box.blockSignals(False)        

    def update_slider(self, key, value):
        """Update slider when parameter is changed."""
        # Block signals to prevent recursion
        self.params_slider[key].blockSignals(True)
        self.params_slider[key].setValue(int(value * self.scale))
        self.params_slider[key].blockSignals(False)         

    def update_spinbox(self, key, value):
        """Update spinbox when parameter is changed."""
        # Block signals to prevent recursion
        self.params_spinbox[key].blockSignals(True)
        self.params_spinbox[key].setValue(value)
        self.params_spinbox[key].blockSignals(False)

    def update_plots(self):
        """Recalculate model and update both plots."""
        A = self.state.element.A
        Z = self.state.element.Z
        B = self.state.element.B
        # Model
        A_model = np.arange(1000) + 1
        B_model = ldm_model(self.state.element, self.state.params, A_model)        

        # Get ranges
        idx_zeros = argrelmin(np.abs(B_model), order=10)[0]

        if B_model[idx_zeros[0]] > 0:
            idx_min = idx_zeros[0] - 1
        else:
            idx_min = idx_zeros[0]

        if B_model[idx_zeros[-1]] < 0:
            idx_max = idx_zeros[-1] - 1
        else:
            idx_max = idx_zeros[-1]

        x_min = np.round(max([-2, A_model[idx_min] * 0.8]))
        x_max = np.round(A_model[idx_max] * 1.2)


        # y_min = round(min(B) * (1 - 0.2), 1)
        y_max = round(max(B) * (1 + 0.2), 1)
        y_min = - 0.1 * y_max

        # Top plot
        self.ax1.clear()
        self.ax1.plot(A, B, "bo", label="Experimental", markersize=4)
        self.ax1.plot(A_model, B_model, "r-", label="Model Gota Líquida")
        self.ax1.axhline(0, color="gray", linestyle="--")
        self.ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        self.ax1.set_xlim(x_min, x_max)
        self.ax1.set_ylim(y_min, y_max)
        self.ax1.set_xlabel("Nombre màssic \n $A$")
        self.ax1.set_ylabel("Energia d'enllaç \n $BE / A$ (MeV)")
        self.ax1.set_title("Gràfica 1")
        self.ax1.legend(loc = 'upper right')
        self.ax1.grid(True)

        self.canvas.draw_idle()

        # Activity 2a, 2b
        # if self.activity_index in (1, 2):
        self.ax1.axvline(x=A_model[idx_max], 
                            color='limegreen', 
                            linestyle='--',
                            label = 'Isòtop més pesat')
        self.ax1.legend(loc='upper right',
                        fontsize=10           # Font size
                        ) 
        
        if self.activity_index in (1, 2):
            self.ax1.axvspan(self.adjust_spinbox['min'].value(),
                             self.adjust_spinbox['max'].value(),
                             color='limegreen',
                             alpha=0.2)
            
    def update_language(self):
        self.activity_mod = load_activity_module(self.state.language, 2)

    def update_text(self):
        # Update text when there's
        # a change of language or 
        # a change of element

        # Get updated activity content
        activity = self.activity_mod.get_activity(self.state)
        
        for section_key, _ in self.sections: 
            scrollbar = self.activity_text[section_key].verticalScrollBar()
            scrollbar_position = scrollbar.value()
            self.activity_text[section_key].setHtml(activity[section_key])
            scrollbar.setValue(scrollbar_position)         

    def update_load_button(self):
        # Enable load button if data exists
        user_data = uc.read_user_info()
        if self.state.element.symbol in user_data:
            self.load_button.setEnabled(True)
        else:
            self.load_button.setEnabled(False)
