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
            En esta actividad, utilizaréis los <strong><em>Parámetros del Modelo de Gota Líquida (MGL)</em></strong> obtenidos en la <strong>Actividad 1</strong> para predecir las propiedades de los isótopos aún no descubiertos.
        </p>  

        <p style="margin: 5px;" align="justify">
            Para que un núcleo pueda existir y no decaiga espontáneamente en las partículas que lo forman, debe tener una energía de enlace positiva (BE/A > 0).
        </p>    

        <p style="margin: 5px; font-size: 12px;" align="justify">
            El número másico (A) del isótopo más pesado aparece en la <strong>Gráfica 1</strong> sobre la línea verde.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>P</font>)
            <strong>¿Cuál es el isótopo más pesado con energía positiva?</strong>
            <br>
            La predicción para el isótopo más pesado de {element.name.split()[-1]} (Z = {element.Z}) es:
            <br>
            A = {A_model[idx_max]}.
        </p>

        <p style="margin: 5px;" align="justify">
            <strong><em>EXTRA:</em></strong>
            ¿Te animas a encontrar el isótopo más pesado de otro elemento?
        </p>
    """,

    "section1" : f"""
        <h4 align="center">Incertidumbre del Parámetro de Asimetría</h4>
        <p style="margin: 5px;" align="justify"> 
            Fijad el parámetro de volumen <i>a<sub>v</sub></i> que encontrasteis en la <strong>Actividad 1</strong>.
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Si guardasteis los valores, podéis pulsar el botón <strong>Cargar</strong>.
        </p>
            
        <p style="margin: 5px;" align="justify"> 
            Supongamos que, para el parámetro de asimetría <i>a<sub>a</sub></i>, cualquier valor del intervalo entre 20 y 25 MeV es posible. 
        </p>

        <p style="margin: 5px;" align="justify"> 
            (<font color='red'>P</font>)
            <em>
            Buscad el rango de predicciones <i>A<sub>min</sub><sup>(aₐ)</sup></i> y <i>A<sub>max</sub><sup>(aₐ)</sup></i> para el isótopo más pesado de {element.name.split()[-1]} (Z = {element.Z}) con energía de enlace positiva.
            </em> 
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Podéis introducir los valores manualmente o utilizar los botones <strong>Fijar</strong>.
            <br>
            El valor fijado será el del isótopo más pesado indicado con la línea verde.
            <br>
            El rango aparece dentro de un área de color verde.
        </p>

        <p style="margin: 5px;" align="justify">
            Una vez ajustado el rango del isótopo más pesado, guardad (<strong>Guardar</strong>) y enviad (<strong>Enviar</strong>) los datos al servidor para compararlos con los de vuestros compañeros/as.
        </p>
    """,

    "section2" : f"""
        <h4 align="center">Incertidumbre del Parámetro de Volumen</h4>
        <p style="margin: 5px;" align="justify"> 
            Fijad el término de asimetría <i>a<sub>v</sub></i> que encontrasteis en la <strong>Actividad 1</strong>.
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Si guardasteis los valores, podéis pulsar el botón <strong>Cargar</strong>.
        </p>
            
        <p style="margin: 5px;" align="justify"> 
            Supongamos que, para el parámetro de volumen <i>a<sub>v</sub></i>, todos los valores del intervalo entre 15 y 17 MeV son posibles. 
        </p>

        <p style="margin: 5px;" align="justify"> 
            (<font color='red'>P</font>)
            <em>
            Buscad el rango de predicciones <i>A<sub>min</sub><sup>(aᵥ)</sup></i> y <i>A<sub>max</sub><sup>(aᵥ)</sup></i> para el isótopo más pesado de {element.name.split()[-1]} (Z = {element.Z}) con energía de enlace positiva.
            </em> 
        </p>

        <p p style="margin: 5px; font-size: 12px;" align="justify">
            Podéis introducir los valores manualmente o utilizar los botones <strong>Fijar</strong>.
            <br>
            El valor fijado será el del isótopo más pesado indicado con la línea verde.
            <br>
            El rango aparece dentro de un área de color verde.
        </p>

        <p style="margin: 5px;" align="justify">
            Una vez ajustado el rango del isótopo más pesado, guardad (<strong>Guardar</strong>) y enviad (<strong>Enviar</strong>) los datos al servidor para compararlos con los de vuestros compañeros.
        </p>
    """
}

def get_info():
        return f"""
                <p style="margin: 5px;" align="center">
                    <font color='red'>
                        <strong> ¿Dudas? Levantad la mano </strong>
                    </font>
                </p> 

                <p style="margin: 5px;" align="justify">
                    Actividades:
                    <br>
                    Podéis moveros entre actividades clicando la pestaña correspondiente.
                    <ul>
                        <li>
                            Actividad 1: Modelo de la Gota Líquida
                        </li>
                        <li>
                            Actividad 2: Predicción de los Isótopos más Pesados
                        </li>
                        <li>
                            Logs: información de la aplicación.
                        </li>
                    </ul> 
                </p>
                
                <p style="margin: 5px;" align="justify">
                    Parámetros:
                    <br>
                    Podéis (des)marcar los parámetros para (des)bloquearlos.
                    <br>
                    Podéis modificar los parámetros:
                    <ul>
                        <li>
                            Escribiendo dentro de las cajas.
                        </li>
                        <li>
                            Usando las flechitas de las cajas.
                        </li>
                        <li>
                            Usando las barras deslizantes.
                        </li>
                    </ul> 
                </p>                  

                <p style="margin: 5px;" align="justify">
                    Gráficas:
                    <ul>
                        <li>
                            La <strong>Gráfica 1</strong> muestra la energía de enlace por nucleón teórica (línea roja) y la medida experimentalmente (puntos azules).
                        </li>
                        <li>
                            Los valores de <i>A<sub>min</sub></i> y <i>A<sub>max</sub></i> pueden introducirse manualmente, con las flechitas o haciendo clic en <strong>Fijar</strong>.
                        </li>
                    </ul>                    
                </p>

                <p style="margin: 5px;" align="justify">
                    Botones:
                    <ul>
                        <li>
                            <strong>Reset</strong> da nuevos valores aleatorios a los parámetros.
                        </li>
                        <li>
                            <strong>Guardar</strong> guarda los parámetros actuales.             
                        </li>
                        <li>
                            <strong>Cargar</strong> carga los parámetros guardados (también los bloqueados).          
                        </li>
                        <li>
                            <strong>Enviar</strong> envía los parámetros guardados al servidor.                           
                        </li>
                        <li>
                            <strong>ⓘ</strong> muestra la ventana de información.                           
                        </li>
                    </ul>                    
                </p>                
            """
