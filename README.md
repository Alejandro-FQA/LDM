This repository contains an application aimed at high school students who participated at the Nuclear Masterclass at Universitat de Barcelona. 

This application consists of a set of exercises where the students have to adjust the parameters of the Liquid Drop Model to experimental data of atomic nuclei.

The application is available in Catalan, Spanish and English. \
Documentation can be found [here](./documentation). \
Executables can be found [here](./dist) (Windows and Linux). 
\
In [Pictures](./pictures) you can find examples (in Catalan) of the application.

**Important**: the online version of the executables should always be stable. \
To compile the executables on your own follow these instructions:

1) create the Python environoment \
`conda create --prefix ./.LDM python=3.11 -y` 
2) activate the environment \
`conda activate ./.LDM` 
3) load the requirements \
`pip install -r requirements.txt`
4) run the command \
`pyinstaller --clean main_window.spec` 
5) run the command \
`pyinstaller --clean server_gui.spec` 

These steps create the executable `main_window` (main app) and `server_gui` (server app) in the directory `dist/` for the current operative system (Windows or Linux). \
It is assumed that you previously downloaded the repository and have conda, Python and pyinstaller installed.

We are happy to hear any feedback!

