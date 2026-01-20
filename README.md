# LDM Application

This repository contains an application aimed at high school students who participated at the Nuclear Masterclass at Universitat de Barcelona.

This application consists of a set of exercises where the students have to adjust the parameters of the Liquid Drop Model to experimental data of atomic nuclei.

The application is available in Catalan, Spanish and English.
Documentation can be found [here](./documentation).
Executables can be found [here](./dist) (Windows and Linux).

**Important**: the online version of the executables should always be stable.

---

## Prerequisites for Building/Modifying

To build the application executables from source or to modify the project, you will need:

*   **Git**: For cloning the repository. Download from [git-scm.com](https://git-scm.com/).
*   **Conda**: For creating and managing the Python development environment (Anaconda or Miniconda recommended). Download from [anaconda.com/download](https://www.anaconda.com/download/) or [repo.anaconda.com/miniconda/](https://repo.anaconda.com/miniconda/).
*   **PyInstaller**: To package the application into executables. It can be installed via pip (`pip install pyinstaller`).

---

## Key Features

*   Appliation for Windows and Linux.
*   Interactive exercises for adjusting Liquid Drop Model parameters.
*   Visualizes experimental data of atomic nuclei.
*   Supports multiple languages: Catalan, Spanish, and English.
*   Includes instructions for compiling executables.
*   Provides documentation and example images.

---

## Screenshots

Example images of the application can be found in the [pictures](./pictures) directory.

---

## Feedback and Support

For feedback or support, please contact the developer at:
alejandro.romero.ros<at>fqa.ub.edu

---

## Building Executables from Source

To compile the executables on your own, follow these instructions:

**Platform-Specific Considerations for Compiling:**

*   **For Windows:**
    *   **Qt Platform Plugin Fix:** In `main_window.py`, ensure the line `os.environ["QT_QPA_PLATFORM"] = "xcb"` is **commented out** (`# os.environ["QT_QPA_PLATFORM"] = "xcb"`). This is crucial to prevent "Qt platform plugin not found" errors.
    *   **PyInstaller Spec Files:** Ensure `main_window.spec` and `server_gui.spec` include the dynamic Qt platform plugin path. Add `from PyQt5.QtCore import QLibraryInfo` at the top and include `(os.path.join(QLibraryInfo.location(QLibraryInfo.PluginsPath), 'platforms'), 'platforms')` in the `datas` array.

*   **For Linux:**
    *   **Qt Platform Plugin Fix:** In `main_window.py`, ensure the line `os.environ["QT_QPA_PLATFORM"] = "xcb"` is **uncommented**. This is often necessary for proper display on Linux systems.

**Compilation Steps:**

1)  **Create the Python environment**:
    ```bash
    conda create --prefix ./.LDM python=3.11 -y
    ```
    *Note: If you encounter a "Terms of Service" error, you may need to accept them using `conda tos accept --override-channels --channel <channel_url>` for each listed channel before retrying.*

2)  **Install dependencies**:
    ```bash
    # On Windows
    conda run -p ./.LDM pip install -r requirements.txt
    # On Linux
    conda activate ./.LDM && pip install -r requirements.txt
    ```
    *Note: If `pip install` encounters issues with `PyQt5-Qt5` or `PyQtWebEngine-Qt5` versions, you may need to edit `requirements.txt` and remove the strict version numbers (e.g., change `PyQt5-Qt5==5.15.17` to `PyQt5-Qt5`).*

3)  **Run PyInstaller for the Main Application**:
    ```bash
    # On Windows
    conda run -p ./.LDM pyinstaller --clean main_window.spec
    # On Linux
    conda activate ./.LDM && pyinstaller --clean main_window.spec
    ```

4)  **Run PyInstaller for the Server Application**:
    ```bash
    # On Windows
    conda run -p ./.LDM pyinstaller --clean server_gui.spec
    # On Linux
    conda activate ./.LDM && pyinstaller --clean server_gui.spec
    ```
These steps create the executable `main_window` (main app) and `server_gui` (server app) in the directory `dist/` for the current operative system (Windows or Linux). 

We are happy to hear any feedback!
