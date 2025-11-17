from ldm_model import ldm_model

def get_activity(state): 

    element = state.element
    params = state.params
    language = state.language

    # Generate table rows from numpy arrays
    B_model = ldm_model(element, params, element.A)
    table_rows = ""
    for i in range(len(element.A)):
        highlight = 'style="background-color: lightgreen;"' \
            if element.A[i] == 2 * element.Z else ""
        table_rows += f"""
                <tr {highlight}>
                    <td align="center">{element.A[i]}</td>
                    <td align="center">{element.B[i]:.3f}</td>
                    <td align="center">{B_model[i]:.3f}</td>
                    <td align="center">{element.B[i] - B_model[i]:.3f}</td>
                </tr>
        """

    table = f"""
            <table border="1" cellpadding="5" cellspacing="1" style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th > </th>
                        <th colspan="2">BE / A (MeV)</th>
                        <th >ΔBE / A (MeV)</th>
                    </tr>
                    <tr style="background-color: #f2f2f2;">
                        <th>A</th>
                        <th>Experimental</th>
                        <th>Theoretical</th>
                        <th>Difference</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            """

   
    return {
    "intro" : """
        <p style="margin: 5px;" align="justify">
            In this activity, you will determine the values of the <strong><em>Liquid Drop Model (LDM) Parameters</em></strong> based on experimental data from known isotopes (data from the <a href="https://www-nds.iaea.org/amdc/" title="mass1.mas20">Atomic Mass Data Center</a>).
        </p>

        <p style="margin: 5px;" align="justify">
            You may revisit Dr. Arnau Rios’ <a href="https://youtu.be/Qsu7IrGiOIk" title="The Liquid Drop Model of Nuclear Binding Energy">video</a> or click the <strong>ⓘ</strong> button for more information.
        </p>

        <p style="margin: 5px;" align="justify">
            Initially, everyone will work with Oxygen.
            <br>
            Afterwards, you will be assigned a random element depending on your group.
        </p>

        <p style="margin: 5px;" align="justify">
            You will have about 10 minutes to complete each section.
            <br>
            <strong>Go to Activity 1a to begin!</strong>
        </p>
    """,

    "section1" : f"""
        <h4 align="center">Adjustment for Oxygen (Z = 8)</h4>
        <p style="margin: 5px;" align="justify">
            In this activity, you will start by adjusting the parameters for Oxygen (Z=8) using the sliders.
        </p>

        <p style="margin: 5px;" align="justify">
            Your goal is to make the difference between the experimental and theoretical values (Graph 2) as close to zero as possible. This process is called parameter optimisation.
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            You can press the <strong>Reset</strong> button to obtain new initial values.
            Any unchecked parameters will remain fixed.
        </p>            

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            <strong>What values did you find?</strong>
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            All energies are given in units of mega–electron-volts (MeV).
        </p>               

        <p style="margin: 5px;" align="justify">
            <strong><em>EXTRA:</em></strong>
            Do you want to try adjusting the parameters for another element?
        </p>

        <p style="margin: 5px;" align="justify">
            <strong>Continue to Activity 1b!</strong>
        </p>
    """,

    "section2" : f"""
        <h4 align="center">Symmetric Isotopes</h4>
        <p style="margin: 5px;" align="justify">
            When an isotope has the same number of protons and neutrons, we say it is symmetric in Z and N.
            This means that the asymmetry term has no effect on the binding energy.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            <em>
            Try changing the asymmetry parameter <i>a<sub>a</sub></i> and verify that the binding energy (Theoretical) calculated for {element.name.split()[-1]} (A = {2 * element.Z}) does not depend on the asymmetry term.
            <br>
            Keep in mind that changing this constant will modify the binding energies of all other isotopes.
            </em>
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            The binding energy value of the symmetric isotope appears in <strong>Graph 1</strong> on the green line and in the <strong>Value Table</strong> highlighted in green.
        </p>
        
        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Value Table:</strong>
            {table}
        </p>
    """,

    "section3" : f"""
        <h4 align="center">Volume Parameter (<i>a<sub>v</sub></i>)</h4>

        <p style="margin: 5px;" align="justify">
            Since the asymmetry term does not affect the binding energy of symmetric isotopes (Activity 1b), we can use this information to determine the volume parameter <i>a<sub>v</sub></i>.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            <em>
            Adjust <i>a<sub>v</sub></i> until the difference between the LDM and the experimental data for {element.name.split()[-1]} (A = {2 * element.Z}) is very close to zero.
            </em>
        </p>
        <p style="margin: 5px; font-size: 12px;" align="justify">
            You may unlock other parameters if you need to refine the fit.
        </p>
        <p style="margin: 5px; font-size: 12px;" align="justify">
            The binding energy value of the symmetric isotope appears in <strong>Graph 1</strong> on the green line and in the <strong>Value Table</strong> highlighted in green.
        </p>

        <p style="margin: 5px;" align="justify">
            Once the volume parameter is adjusted, save (<strong>Save</strong>) and submit (<strong>Submit</strong>) the data to the server to compare with your classmates.
        </p>

        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Value Table:</strong>
            {table}
        </p>
    """,

    "section4" : f"""
        <h4 align="center">Asymmetry Parameter (<i>a<sub>a</sub></i>)</h4>

        <p style="margin: 5px;" align="justify">
            Now that you know the volume parameter <i>a<sub>v</sub></i> (Activity 1c), you can determine the asymmetry parameter <i>a<sub>a</sub></i> for all isotopes of {element.name.split()[-1]} (Z = {element.Z}) shown in the graphs. 
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            <em>
            Adjust <i>a<sub>a</sub></i> until the shape of the theoretical binding energy curve (red line) matches the experimental data (blue points) in <strong>Graph 1</strong>. 
            This should also minimise the difference shown in <strong>Graph 2</strong> (more points near zero). 
            </em>
        </p>
        <p style="margin: 5px; font-size: 12px;" align="justify">
            You may unlock other parameters if you need to refine the fit.
        </p>
        <p style="margin: 5px; font-size: 12px;" align="justify">
            The final answer should be accurate to about 1 MeV.
        </p> 

        <p style="margin: 5px;" align="justify">
            Once the parameter is adjusted, save (<strong>Save</strong>) and submit (<strong>Submit</strong>) the data to the server to compare with your classmates.
        </p>

        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Value Table:</strong>
            {table}
        </p>
    """,

    "section5" : f"""
        <h4 align="center">Pairing Parameter (<i>a<sub>p</sub></i>)</h4>

        <p style="margin: 5px;" align="justify">
            Now that you have determined both the volume parameter <i>a<sub>v</sub></i> (Activity 1c) and the asymmetry parameter <i>a<sub>a</sub></i> (Activity 1d) of the LDM, we can investigate the effect of the pairing term.
        </p>                

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            <em>
            Set <i>a<sub>p</sub></i> = 0 while keeping the parameters <i>a<sub>v</sub></i> and <i>a<sub>a</sub></i> fixed at the values found in the previous activities.
            <br>
            In <strong>Graph 2</strong> you will observe a surprising effect depending on whether {element.name.split()[-1]} (Z = {element.Z}) has an even or odd number of nucleons.
            <br>
            This is the effect of the pairing term described in the video by Dr. Arnau Rios (<a href="https://www.youtube.com/watch?v=Qsu7IrGiOIk">youtube.com</a>).
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            The isotopes with A=13 and A=17 are shown in <strong>Graph 1</strong> and <strong>Graph 2</strong> with grey lines.
        </p>
        <p style="margin: 5px; font-size: 12px;" align="justify">
            You may load the saved values from the previous activities using the <strong>Load</strong> button.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            What is the scale of the differences you observe in <strong>Graph 2</strong> (in MeV)?
            <br>
            (<font color='red'>Q</font>)
            How does this compare to the total binding energy per nucleon (in MeV) in <strong>Graph 1</strong>?
            <br>
            [Note: You do not need to record the answers to this question.]
            </em>
        </p>

        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Value Table:</strong>
            {table}
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
                    You may move between activities by clicking the corresponding tab.
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
                    You may change the parameters:
                    <ul>
                        <li>
                            By typing inside the boxes.
                        </li>
                        <li>
                            Using the arrows inside the boxes.
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
                            <strong>Graph 2</strong> shows the difference between experimental and theoretical binding energies.
                            The smaller the RMS error, the better the theoretical model.
                        </li>
                    </ul>                    
                </p>

                
                
                <p style="margin: 5px;" align="justify">
                    Buttons:
                    <ul>
                        <li>
                            <strong>Reset</strong> gives new random parameter values.
                        </li>
                        <li>
                            <strong>Save</strong> stores the current parameters.             
                        </li>
                        <li>
                            <strong>Load</strong> loads the saved parameters (locked ones as well).          
                        </li>
                        <li>
                            <strong>Submit</strong> sends the saved parameters to the server.                           
                        </li>
                        <li>
                            <strong>ⓘ</strong> shows the information window.                           
                        </li>
                    </ul>                    
                </p>                
            """
