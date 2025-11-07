from ldm_model import ldm_model

def get_activity(activity, state): 

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
                        <th>Teòrica</th>
                        <th>Diferència</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            """

    match activity:
        case 1:
            return {
            "intro" : """
                <p style="margin: 5px;" align="justify">
                    En aquesta activitat, determinareu els valors dels <strong><em>Paràmetres del Model de Gota Líquida (MGL)</em></strong> basant-vos en les dades experimentals d'isòtops coneguts (dades de l' <a href="https://www-nds.iaea.org/amdc/" title="mass1.mas20">Atomic Mass Data Center</a>).
                </p>

                <p style="margin: 5px;" align="justify">
                    Podeu tornar a visitar el <a href="https://youtu.be/Qsu7IrGiOIk" title="The Liquid Drop Model of Nuclear Binding Energy">vídeo</a> del Dr. Arnau Rios o clicar el botó <strong>ⓘ</strong> per més informació.
                </p>

                <p style="margin: 5px;" align="justify">
                    Inicialment, tothom treballarà amb l'Oxigen.
                    <br>
                    Després s'us assignarà un element aleatori en funció del grup.
                </p>

                <p style="margin: 5px;" align="justify">
                    Tindreu uns 10 minuts per completar cada apartat.
                    <br>
                    <strong>Passeu a l'Activitat 1a per començar!</strong>
                </p>
            """,
            "section1" : f"""
                <h4 align="center">Ajust per l'Oxigen (Z = 8)</h4>
                <p style="margin: 5px;" align="justify">
                    En aquesta activitat, començareu ajustant els paràmetres per a l'Oxigen (Z=8) fent servir les barres lliscants.
                </p>

                <p style="margin: 5px;" align="justify">
                    El vostre objectiu és que la diferència entre els valors experimentals i teòrics (Gràfica 2) sigui el més propera de zero. D'això se'n diu optimitzar els paràmetres.
                </p>

                <p style="margin: 5px; font-size: 12px;" align="justify">
                    Podeu prémer el botó <strong>Reseteja</strong> per obtenir uns nous valors inicials.
                    Els paràmetres desmarcats romandran fixes.
                </p>            

                <p style="margin: 5px;" align="justify">
                    (<font color='red'>Q</font>)
                    <strong>Quins valors heu trobat?</strong>
                </p>
                <p style="margin: 5px; font-size: 12px;" align="justify">
                    Totes les energies es donen en unitats de megaelectró-volts (MeV).
                </p>               

                <p style="margin: 5px;" align="justify">
                    <strong><em>EXTRA:</em></strong>
                    T'animes a ajustar els paràmetres per un altre element?
                </p>

                <p style="margin: 5px;" align="justify">
                    <strong>Passeu a l'Activitat 1b per continuar!</strong>
                </p>
            """,
            "section2" : f"""
                <h4 align="center">Isòtops simètrics</h4>
                <p style="margin: 5px;" align="justify">
                    Quan un isòtop té el mateix nombre de protons i neutrons, diem que és simètric en Z i N.
                    Això significa que el terme d'asimetria no té cap efecte sobre l'energia d'enllaç.
                </p>

                <p style="margin: 5px;" align="justify">
                    (<font color='red'>Q</font>)
                    <em>
                    Proveu de canviar el paràmetre d'asimetria <i>a<sub>a</sub></i> i convenceu-vos que l'energia d'enllaç (Teòrica) calculada per al {element.name.split()[-1]} (A = {2 * element.Z}) no depèn del terme d'asimetria. 
                    <br>
                    Tingueu en compte que el canvi de constant modificarà les energies d'enllaç de tots els altres isòtops.
                    </em>
                </p>

                <p style="margin: 5px; font-size: 12px;" align="justify">
                    El valor de l'energia d'enllaç de l'isòtop simètric apareix a la <strong>Gràfica 1</strong> sobre la línia verda i a la <strong>Taula de valors</strong> resaltat en verd.
                </p>
                
                <p style="margin: 5px;" align="justify">
                    <br>
                    <strong>Taula de valors:</strong>
                    {table}
                </p>
            """,
            "section3" : f"""
                <h4 align="center">Paràmetre de Volum (<i>a<sub>v</sub></i>)</h4>

                <p style="margin: 5px;" align="justify">
                    Atès que el terme d'asimetria no afecta l'energia d'enllaç dels isòtops simètrics (Activitat 1b), podem fer servir aquesta informació per determinar el paràmetre de volum <i>a<sub>v</sub></i>.
                </p>

                <p style="margin: 5px;" align="justify">
                    (<font color='red'>Q</font>)
                    <em>
                    Modifiqueu <i>a<sub>v</sub></i> fins que la diferència entre el MGL i les dades experimentals del {element.name.split()[-1]} (A = {2 * element.Z}) sigui molt propera a zero.
                    </em>
                </p>
                <p style="margin: 5px; font-size: 12px;" align="justify">
                    Podeu desbloquejar altres paràmetres si necessiteu afinar l'ajust.
                </p>
                <p style="margin: 5px; font-size: 12px;" align="justify">
                    El valor de l'energia d'enllaç de l'isòtop simètric apareix a la <strong>Gràfica 1</strong> sobre la línia verda i a la <strong>Taula de valors</strong> resaltat en verd.
                </p>

                <p style="margin: 5px;" align="justify">
                    Un cop ajustat el paràmetre de volum, deseu (<strong>Desa</strong>) i envieu (<strong>Envia</strong>) les dades al servidor per comparar-les amb les dels companys/es.
                </p>

                <p style="margin: 5px;" align="justify">
                    <br>
                    <strong>Taula de valors:</strong>
                    {table}
                </p>
            """,
            "section4" : f"""
                <h4 align="center">Paràmetre d'Asimetria (<i>a<sub>a</sub></i>)</h4>

                <p style="margin: 5px;" align="justify">
                    Ara que ja sabeu quin és el paràmetre de volum <i>a<sub>v</sub></i> (Activitat 1c), podeu determinar el paràmetre d'asimetria <i>a<sub>a</sub></i> per tots els isòtops de {element.name.split()[-1]} (Z = {element.Z}) que es mostren a les gràfiques. 
                </p>

                <p style="margin: 5px;" align="justify">
                    (<font color='red'>Q</font>)
                    <em>
                    Modifiqueu <i>a<sub>a</sub></i> fins que la forma de la corba d'energia d'enllaç teòrica (línia vermella) coincideixi amb les dades experimentals (punts blaus) de la <strong>Gràfica 1</strong>. 
                    Això també hauria de minimitzar la diferència representada a la <strong>Gràfica 2</strong> (més punts propers a zero). 
                    </em>
                </p>
                <p style="margin: 5px; font-size: 12px;" align="justify">
                    Podeu desbloquejar altres paràmetres si necessiteu afinar l'ajust.
                </p>
                <p p style="margin: 5px; font-size: 12px;" align="justify">
                    La resposta final ha de tenir una precisió aproximada de 1 MeV.
                </p> 

                <p style="margin: 5px;" align="justify">
                    Un cop ajustat el paràmetre de volum, deseu (<strong>Desa</strong>) i envieu (<strong>Envia</strong>) les dades al servidor per comparar-les amb les dels companys.
                </p>

                <p style="margin: 5px;" align="justify">
                    <br>
                    <strong>Taula de valors:</strong>
                    {table}
                </p>
            """,
            "section5" : f"""
                <h4 align="center">Paràmetre d'Aparellament (<i>a<sub>p</sub></i>)</h4>

                <p style="margin: 5px;" align="justify">
                    Ara que heu determinat tant el paràmetre de volum <i>a<sub>v</sub></i> (Activitat 1c) com el paràmetre d'asimetria <i>a<sub>v</sub></i> (Activitat 1d) del MGL, podem investigar l'efecte del terme d'aparellament.
                </p>                

                <p style="margin: 5px;" align="justify">
                    (<font color='red'>Q</font>)
                    <em>
                    Definiu <i>a<sub>p</sub></i> = 0, mantenint fixes els paràmetres <i>a<sub>v</sub></i> i <i>a<sub>a</sub></i> trobats en les activitats anteriors.
                    <br>
                    A la <strong>Gràfica 2</strong> hi veureu un efecte sorprenent en funció de si el {element.name.split()[-1]} (Z = {element.Z}) té un nombre parell o senar de nucleons.
                    <br>
                    Aquest és l'efecte del terme d'emparellament explicat al vídeo pel doctor Arnau Rios (<a href="https://www.youtube.com/watch?v=Qsu7IrGiOIk">youtube.com</a>).
                </p>

                <p p style="margin: 5px; font-size: 12px;" align="justify">
                    Els isòtops amb A=13 i A=17 estan indicats a les <strong>Gràfica 1</strong> i <strong>Gràfica 2</strong> amb línies grises.
                </p>
                <p style="margin: 5px; font-size: 12px;" align="justify">
                    Podeu carregar els valos guardats de les activitats anteriors amb el botó <strong>Carrega</strong>.
                </p>

                <p style="margin: 5px;" align="justify">
                    (<font color='red'>Q</font>)
                    Quina és l'escala de les diferències que veieu a la  <strong>Gràfica 2</strong> (en MeV)?
                    <br>
                    (<font color='red'>Q</font>)
                    Com es compara això amb l'energia d'enllaç total per nucleó (en MeV) de la <strong>Gràfica 1</strong>?
                    <br>
                    [Nota: no cal que registreu les respostes a aquesta pregunta]
                    </em>
                </p>

                <p style="margin: 5px;" align="justify">
                    <br>
                    <strong>Taula de valors:</strong>
                    {table}
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
                            Escrivint dins de les capses.
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
                            La <strong>Gràfica 2</strong> mostra la diferència entre les energies d'enllaç experimental i teòrica.
                            Com més petit sigui l'error RMS, millor serà el model teòric.
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