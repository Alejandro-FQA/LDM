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
            En aquesta activitat, fareu servir els <strong><em>Paràmetres del Model de Gota Líquida (MGL)</em></strong> trobats a l'<strong>Activitat 1</strong> per predir les propietats dels isòtops encara no descoberts.
        </p>  

        <p style="margin: 5px;" align="justify">
            Per tal que un nucli pugui existir, i no decaigui espontàniament en les partícules que el conformen, ha de tenir una energia d'enllaç positiva (BE/A > 0).
        </p>    

        <p style="margin: 5px; font-size: 12px;" align="justify">
            El nombre màssic (A) de l'isòtop més pesat apareix a la <strong>Gràfica 1</strong> sobre la línia verda.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>Q</font>)
            <strong>Quins és l'isòtop més pesat amb energia positiva?</strong>
            <br>
            Predicció de l'isòtop més pesat del {element.name.split()[-1]} (Z = {element.Z}) és:
            <br>
            A = {A_model[idx_max]}.
        </p>

        <p style="margin: 5px;" align="justify">
            <strong><em>EXTRA:</em></strong>
            T'animes a trobar l'isòtop més pesat d'un altre element?
        </p>
    """,
    "section1" : f"""
        <h4 align="center">Incertesa del Paràmetre d'Asimetria</h4>
        <p style="margin: 5px;" align="justify"> 
            Fixeu el paràmetre de volum <i>a<sub>v</sub></i> que heu trobat en l'<strong>Activitat 1</strong>.
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Si heu guardat els valors, podeu prémer el botó <strong>Carrega</strong>.
        </p>
            
        <p style="margin: 5px;" align="justify"> 
            Suposem que, per al paràmetre d'asimetria <i>a<sub>a</sub></i>, tots els valors de l'interval entre 20 i 25 MeV són possibles. 
        </p>
        <p style="margin: 5px;" align="justify"> 
            (<font color='red'>Q</font>)
            <em>
            Busqueu el rang de prediccions <i>A<sub>min</sub><sup>(aₐ)</sup></i> i <i>A<sub>max</sub><sup>(aₐ)</sup></i> per a l'isòtop de {element.name.split()[-1]} (Z = {element.Z}) més pesat amb una energia d'enllaç positiva.
            </em> 
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Podeu introduir els valors manualment o fent servir els botons <strong>Fixa</strong>.
            <br>
            El valor fixat serà el de l'isòtop més pesat indicat amb la línia verda.
            <br>
            El rang es mostra dins una àrea de color verd.
        </p>

        <p style="margin: 5px;" align="justify">
            Un cop ajustat el rang de l'isòtop més pesat, deseu (<strong>Desa</strong>) i envieu (<strong>Envia</strong>) les dades al servidor per comparar-les amb les dels companys/es.
        </p>
        
    """,
    "section2" : f"""
        <h4 align="center">Incertesa del Paràmetre de Volum</h4>
        <p style="margin: 5px;" align="justify"> 
            Fixeu el terme d'asimetria <i>a<sub>v</sub></i> que heu trobat en l'<strong>Activitat 1</strong>.
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Si heu guardat els valors, podeu prémer el botó <strong>Carrega</strong>.
        </p>
            
        <p style="margin: 5px;" align="justify"> 
            Suposem que, per al paràmetre de volum <i>a<sub>v</sub></i>, tots els valors de l'interval entre 15 i 17 MeV són possibles. 
        </p>
        <p style="margin: 5px;" align="justify"> 
            (<font color='red'>Q</font>)
            <em>
            Busqueu el rang de prediccions <i>A<sub>min</sub><sup>(aᵥ)</sup></i> i <i>A<sub>max</sub><sup>(aᵥ)</sup></i> per a l'isòtop de {element.name.split()[-1]} (Z = {element.Z}) més pesat amb una energia d'enllaç positiva.
            </em> 
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Podeu introduir els valors manualment o fent servir els botons <strong>Fixa</strong>.
            <br>
            El valor fixat serà el de l'isòtop més pesat indicat amb la línia verda.
            <br>
            El rang es mostra dins una àrea de color verd.
        </p>

        <p style="margin: 5px;" align="justify">
            Un cop ajustat el rang de l'isòtop més pesat, deseu (<strong>Desa</strong>) i envieu (<strong>Envia</strong>) les dades al servidor per comparar-les amb les dels companys.
        </p>
    """
}

def get_info():
        return f"""
                <p style="margin: 5px;" align="center">
                    <font color='red'>
                        <strong> Dubtes? Aixequeu la mà </strong>
                    </font>
                </p> 

                <p style="margin: 5px;" align="justify">
                    Activitats:
                    <br>
                    Podeu moure-us entre activitats clicant la pestanya corresponent.
                    <ul>
                        <li>
                            Activitat 1: Model de la Gota Líquida
                        </li>
                        <li>
                            Activitat 2: Predicció dels Isòtops més pesats
                        </li>
                        <li>
                            Logs: informació de l'aplicatiu.
                        </li>
                    </ul> 
                </p>
                
                <p style="margin: 5px;" align="justify">
                    Pràmetres:
                    <br>
                    Podeu (des)marcar els paràmetres per (des)bloquejar-los.
                    <br>
                    Podeu canviar els paràmetres:
                    <ul>
                        <li>
                            Escribint dins de les capses.
                        </li>
                        <li>
                            Amb les fletxetes de les capses.
                        </li>
                        <li>
                            Amb les barres lliscants.
                        </li>
                    </ul> 
                </p>                  

                <p style="margin: 5px;" align="justify">
                    Gràfiques:
                    <ul>
                        <li>
                            La <strong>Gràfica 1</strong> mostra l'energia d'enllaç per nucleó teòrica (línia vermella) i la mesurada experimentalment (punts blaus).
                        </li>
                        <li>
                            Els valors de <i>A<sub>min</sub></i> i <i>A<sub>max</sub></i> es poden introduir a mà, amb les fletxetes o clicant <strong>Fixa</strong>.
                        </li>
                    
                    </ul>                    
                </p>

                
                
                <p style="margin: 5px;" align="justify">
                    Botons:
                    <ul>
                        <li>
                            <strong>Reset</strong> dona nous valors aleatoris als paràmetres.
                        </li>
                        <li>
                            <strong>Desa</strong> guarda els paràmetres actuals.             
                        </li>
                        <li>
                            <strong>Carrega</strong> carrega els paràmetres guardats (bloquejats també).          
                        </li>
                        <li>
                            <strong>Envia</strong> envia els paràmetres guardats al servidor.                           
                        </li>
                        <li>
                            <strong>ⓘ</strong> mostra la finestra d'informació.                           
                        </li>
                    </ul>                    
                </p>                
            """