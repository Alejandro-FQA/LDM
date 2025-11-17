from ldm_model import ldm_model
import numpy as np
from scipy.signal import argrelmin


def get_activity(state): 

    element = state.element
    params = state.params
    language = state.language

    # Find the zeros of the binding energy
    A_model = np.arange(1000) + 1
    B_model = ldm_model(element, params, A_model)
    idx_zeros = argrelmin(np.abs(B_model), order=10)[0]
    if B_model[idx_zeros[-1]] < 0:
        idx_max = idx_zeros[-1] - 1
    else:
        idx_max = idx_zeros[-1]


    return {
    "intro" : f"""
        <p style="margin: 5px;" align="justify">
            In this activity, you will use the <strong><em>Liquid Drop Model (LDM) Parameters</em></strong> found in <strong>Activity 1</strong> to predict the properties of isotopes that have not yet been discovered.
        </p>  

        <p style="margin: 5px;" align="justify">
            For a nucleus to exist and not spontaneously decay into its constituent particles, it must have a positive binding energy (BE/A > 0).
        </p>    

        <p style="margin: 5px; font-size: 12px;" align="justify">
            The mass number (A) of the heaviest isotope appears in <strong>Graph 1</strong> on the green line.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            <strong>What is the heaviest isotope with positive energy?</strong>
            <br>
            The prediction for the heaviest isotope of {element.name.split()[-1]} (Z = {element.Z}) is:
            <br>
            A = {A_model[idx_max]}.
        </p>

        <p style="margin: 5px;" align="justify">
            <strong><em>EXTRA:</em></strong>
            Do you want to try finding the heaviest isotope of another element?
        </p>
    """,

    "section1" : f"""
        <h4 align="center">Uncertainty of the Asymmetry Parameter</h4>
        <p style="margin: 5px;" align="justify"> 
            Fix the volume parameter <i>a<sub>v</sub></i> that you found in <strong>Activity 1</strong>.
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            If you saved the values, you can press the <strong>Load</strong> button.
        </p>
            
        <p style="margin: 5px;" align="justify"> 
            Let us assume that, for the asymmetry parameter <i>a<sub>a</sub></i>, any value in the interval between 20 and 25 MeV is possible. 
        </p>

        <p style="margin: 5px;" align="justify"> 
            (<font color='red'>Q</font>)
            <em>
            Find the prediction range <i>A<sub>min</sub><sup>(aₐ)</sup></i> and <i>A<sub>max</sub><sup>(aₐ)</sup></i> for the heaviest isotope of {element.name.split()[-1]} (Z = {element.Z}) with positive binding energy.
            </em> 
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            You may enter the values manually or use the <strong>Fix</strong> buttons.
            <br>
            The fixed value will be that of the heaviest isotope indicated by the green line.
            <br>
            The range is shown inside a green-shaded area.
        </p>

        <p style="margin: 5px;" align="justify">
            Once the range of the heaviest isotope is adjusted, save (<strong>Save</strong>) and submit (<strong>Submit</strong>) the data to the server to compare with your classmates.
        </p>
    """,

    "section2" : f"""
        <h4 align="center">Uncertainty of the Volume Parameter</h4>
        <p style="margin: 5px;" align="justify"> 
            Fix the asymmetry parameter <i>a<sub>v</sub></i> that you found in <strong>Activity 1</strong>.
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            If you saved the values, you can press the <strong>Load</strong> button.
        </p>
            
        <p style="margin: 5px;" align="justify"> 
            Let us assume that, for the volume parameter <i>a<sub>v</sub></i>, all values in the interval between 15 and 17 MeV are possible. 
        </p>

        <p style="margin: 5px;" align="justify"> 
            (<font color='red'>Q</font>)
            <em>
            Find the prediction range <i>A<sub>min</sub><sup>(aᵥ)</sup></i> and <i>A<sub>max</sub><sup>(aᵥ)</sup></i> for the heaviest isotope of {element.name.split()[-1]} (Z = {element.Z}) with positive binding energy.
            </em> 
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            You may enter the values manually or use the <strong>Fix</strong> buttons.
            <br>
            The fixed value will be that of the heaviest isotope indicated by the green line.
            <br>
            The range is shown inside a green-shaded area.
        </p>

        <p style="margin: 5px;" align="justify">
            Once the range of the heaviest isotope is adjusted, save (<strong>Save</strong>) and submit (<strong>Submit</strong>) the data to the server to compare with your classmates.
        </p>
    """
}

def get_info():
        return f"""
                <p style="margin: 5px;" align="center">
                    <font color='red'>
                        <strong> Questions? Raise your hand </strong>
                    </font>
                </p> 

                <p style="margin: 5px;" align="justify">
                    Activities:
                    <br>
                    You can move between activities by clicking the corresponding tab.
                    <ul>
                        <li>
                            Activity 1: Liquid Drop Model
                        </li>
                        <li>
                            Activity 2: Prediction of the Heaviest Isotopes
                        </li>
                        <li>
                            Logs: application information.
                        </li>
                    </ul> 
                </p>
                
                <p style="margin: 5px;" align="justify">
                    Parameters:
                    <br>
                    You may (un)check parameters to (un)lock them.
                    <br>
                    You may modify the parameters:
                    <ul>
                        <li>
                            By typing inside the boxes.
                        </li>
                        <li>
                            Using the arrows in the boxes.
                        </li>
                        <li>
                            Using the sliders.
                        </li>
                    </ul> 
                </p>                  

                <p style="margin: 5px;" align="justify">
                    Graphs:
                    <ul>
                        <li>
                            <strong>Graph 1</strong> shows the theoretical binding energy per nucleon (red line) and the experimentally measured values (blue points).
                        </li>
                        <li>
                            The values of <i>A<sub>min</sub></i> and <i>A<sub>max</sub></i> can be entered manually, with the arrows, or by clicking <strong>Fix</strong>.
                        </li>
                    </ul>                    
                </p>

                <p style="margin: 5px;" align="justify">
                    Buttons:
                    <ul>
                        <li>
                            <strong>Reset</strong> assigns new random parameter values.
                        </li>
                        <li>
                            <strong>Save</strong> stores the current parameters.             
                        </li>
                        <li>
                            <strong>Load</strong> loads the saved parameters (including locked ones).          
                        </li>
                        <li>
                            <strong>Submit</strong> sends the saved parameters to the server.                           
                        </li>
                        <li>
                            <strong>ⓘ</strong> opens the information window.                           
                        </li>
                    </ul>                    
                </p>                
            """
