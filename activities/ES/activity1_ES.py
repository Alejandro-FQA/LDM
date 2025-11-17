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
                        <th>Teórica</th>
                        <th>Diferencia</th>
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
            En esta actividad, determinaréis los valores de los <strong><em>Parámetros del Modelo de Gota Líquida (MGL)</em></strong> basándoos en los datos experimentales de isótopos conocidos (datos del <a href="https://www-nds.iaea.org/amdc/" title="mass1.mas20">Atomic Mass Data Center</a>).
        </p>

        <p style="margin: 5px;" align="justify">
            Podéis volver a ver el <a href="https://youtu.be/Qsu7IrGiOIk" title="The Liquid Drop Model of Nuclear Binding Energy">vídeo</a> del Dr. Arnau Rios o pulsar el botón <strong>ⓘ</strong> para más información.
        </p>

        <p style="margin: 5px;" align="justify">
            Inicialmente, todo el mundo trabajará con el Oxígeno.
            <br>
            Después se os asignará un elemento aleatorio según el grupo.
        </p>

        <p style="margin: 5px;" align="justify">
            Tendréis unos 10 minutos para completar cada apartado.
            <br>
            <strong>¡Pasad a la Actividad 1a para empezar!</strong>
        </p>
    """,

    "section1" : f"""
        <h4 align="center">Ajuste para el Oxígeno (Z = 8)</h4>
        <p style="margin: 5px;" align="justify">
            En esta actividad comenzaréis ajustando los parámetros para el Oxígeno (Z=8) usando las barras deslizantes.
        </p>

        <p style="margin: 5px;" align="justify">
            El objetivo es que la diferencia entre los valores experimentales y los teóricos (Gráfica 2) sea lo más cercana posible a cero. Esto se llama optimizar los parámetros.
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            Podéis pulsar el botón <strong>Reiniciar</strong> para obtener nuevos valores iniciales.
            Los parámetros desmarcados permanecerán fijos.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>P</font>)
            <strong>¿Qué valores habéis encontrado?</strong>
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            Todas las energías se dan en unidades de megaelectrón-voltios (MeV).
        </p>

        <p style="margin: 5px;" align="justify">
            <strong><em>EXTRA:</em></strong>
            ¿Te animas a ajustar los parámetros para otro elemento?
        </p>

        <p style="margin: 5px;" align="justify">
            <strong>¡Pasad a la Actividad 1b para continuar!</strong>
        </p>
    """,

    "section2" : f"""
        <h4 align="center">Isótopos simétricos</h4>
        <p style="margin: 5px;" align="justify">
            Cuando un isótopo tiene el mismo número de protones y neutrones, decimos que es simétrico en Z y N.
            Esto significa que el término de asimetría no tiene ningún efecto sobre la energía de enlace.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>P</font>)
            <em>
            Probad a cambiar el parámetro de asimetría <i>a<sub>a</sub></i> y comprobad que la energía de enlace (Teórica) calculada para el {element.name.split()[-1]} (A = {2 * element.Z}) no depende del término de asimetría.
            <br>
            Tened en cuenta que cambiar esta constante modificará las energías de enlace de todos los demás isótopos.
            </em>
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            El valor de la energía de enlace del isótopo simétrico aparece en la <strong>Gráfica 1</strong> sobre la línea verde y en la <strong>Tabla de valores</strong> resaltado en verde.
        </p>

        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Tabla de valores:</strong>
            {table}
        </p>
    """,

    "section3" : f"""
        <h4 align="center">Parámetro de Volumen (<i>a<sub>v</sub></i>)</h4>

        <p style="margin: 5px;" align="justify">
            Dado que el término de asimetría no afecta la energía de enlace de los isótopos simétricos (Actividad 1b), podemos usar esta información para determinar el parámetro de volumen <i>a<sub>v</sub></i>.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>P</font>)
            <em>
            Modificad <i>a<sub>v</sub></i> hasta que la diferencia entre el MGL y los datos experimentales del {element.name.split()[-1]} (A = {2 * element.Z}) sea muy cercana a cero.
            </em>
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            Podéis desbloquear otros parámetros si necesitáis afinar el ajuste.
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            El valor de la energía de enlace del isótopo simétrico aparece en la <strong>Gráfica 1</strong> sobre la línea verde y en la <strong>Tabla de valores</strong> resaltado en verde.
        </p>

        <p style="margin: 5px;" align="justify">
            Una vez ajustado el parámetro de volumen, guardad (<strong>Guardar</strong>) y enviad (<strong>Enviar</strong>) los datos al servidor para compararlos con los de vuestros compañeros/as.
        </p>

        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Tabla de valores:</strong>
            {table}
        </p>
    """,

    "section4" : f"""
        <h4 align="center">Parámetro de Asimetría (<i>a<sub>a</sub></i>)</h4>

        <p style="margin: 5px;" align="justify">
            Ahora que ya conocéis el parámetro de volumen <i>a<sub>v</sub></i> (Actividad 1c), podéis determinar el parámetro de asimetría <i>a<sub>a</sub></i> para todos los isótopos de {element.name.split()[-1]} (Z = {element.Z}) que se muestran en las gráficas.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>P</font>)
            <em>
            Modificad <i>a<sub>a</sub></i> hasta que la forma de la curva de energía de enlace teórica (línea roja) coincida con los datos experimentales (puntos azules) de la <strong>Gráfica 1</strong>.
            Esto también debería minimizar la diferencia representada en la <strong>Gráfica 2</strong> (más puntos cercanos a cero).
            </em>
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            Podéis desbloquear otros parámetros si necesitáis afinar el ajuste.
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            La respuesta final debe tener una precisión aproximada de 1 MeV.
        </p>

        <p style="margin: 5px;" align="justify">
            Una vez ajustado el parámetro, guardad (<strong>Guardar</strong>) y enviad (<strong>Enviar</strong>) los datos al servidor para compararlos con los de vuestros compañeros.
        </p>

        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Tabla de valores:</strong>
            {table}
        </p>
    """,

    "section5" : f"""
        <h4 align="center">Parámetro de Apareamiento (<i>a<sub>p</sub></i>)</h4>

        <p style="margin: 5px;" align="justify">
            Ahora que habéis determinado tanto el parámetro de volumen <i>a<sub>v</sub></i> (Actividad 1c) como el parámetro de asimetría <i>a<sub>a</sub></i> (Actividad 1d) del MGL, podemos investigar el efecto del término de pareamiento.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>P</font>)
            <em>
            Definid <i>a<sub>p</sub></i> = 0, manteniendo fijos los parámetros <i>a<sub>v</sub></i> y <i>a<sub>a</sub></i> obtenidos en las actividades anteriores.
            <br>
            En la <strong>Gráfica 2</strong> veréis un efecto sorprendente según si el {element.name.split()[-1]} (Z = {element.Z}) tiene un número par o impar de nucleones.
            <br>
            Este es el efecto del término de emparejamiento explicado en el vídeo por el doctor Arnau Rios (<a href="https://www.youtube.com/watch?v=Qsu7IrGiOIk">youtube.com</a>).
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            Los isótopos con A=13 y A=17 están indicados en la <strong>Gráfica 1</strong> y la <strong>Gráfica 2</strong> con líneas grises.
        </p>

        <p style="margin: 5px; font-size: 12px;" align="justify">
            Podéis cargar los valores guardados de actividades anteriores con el botón <strong>Cargar</strong>.
        </p>

        <p style="margin: 5px;" align="justify">
            (<font color='red'>P</font>)
            ¿Cuál es la escala de las diferencias que observáis en la <strong>Gráfica 2</strong> (en MeV)?
            <br>
            (<font color='red'>P</font>)
            ¿Cómo se compara esto con la energía de enlace total por nucleón (en MeV) de la <strong>Gráfica 1</strong>?
            <br>
            [Nota: no es necesario registrar las respuestas de esta pregunta]
            </em>
        </p>

        <p style="margin: 5px;" align="justify">
            <br>
            <strong>Tabla de valores:</strong>
            {table}
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
                    Podéis moveros entre actividades haciendo clic en la pestaña correspondiente.
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
                    Podéis cambiar los parámetros:
                    <ul>
                        <li>
                            Escribiendo dentro de las cajas.
                        </li>
                        <li>
                            Con las flechitas de las cajas.
                        </li>
                        <li>
                            Con las barras deslizantes.
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
                            La <strong>Gráfica 2</strong> muestra la diferencia entre las energías de enlace experimental y teórica.
                            Cuanto más pequeño sea el error RMS, mejor será el modelo teórico.
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
                            <strong>Cargar</strong> carga los parámetros guardados (bloqueados también).
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
