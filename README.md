This repository contains an application aimed at high school students. \
This application is a set of exercises where the students have to adjust the parameters of the Liquid Drop Model to experimental data of atomic nuclei.

It is currently only available in Catalan. \
Spanish and English will follow. \
Compiled versions can be found in `dist/` called `main_window`(Windows and Linux).

Once you have created the Python environoment \
`conda env create --prefix ./.LDM -f environment.yml` \
you can activate it \
`conda activate ./.LDM` \
and run \
`pyinstaller --onefile --windowed --add-data "atomic_mass.txt:." main_window.py` \
to create the executable. \
It creates the executable in `dist/` called `main_window` for the current operative system (Windows or Linux).
 
In [Pictures](./pictures) you can find examples of the application.
