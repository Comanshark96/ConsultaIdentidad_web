import sys
from io import BytesIO
from base64 import b64decode
import requests
import mechanicalsoup
import pytesseract
from PIL import Image


def poner_guiones(identidad):
    """ Pone los guiones a las identidades """

    identidad_guiones = str()
    lista_identidad = list(identidad)
    lista_identidad.insert(4, '-')
    lista_identidad.insert(9, '-')

    for caracter in lista_identidad:
        identidad_guiones += caracter

    return identidad_guiones

class ConsultaIdentidad:
    """ Consulta la identidad de un ciudadano en la base de datos del RNP.
    """

    _navegador = mechanicalsoup.StatefulBrowser()
    _url = 'http://www.rnp.hn/estadEnrolamiento/consulta_por_identidad'

    def __init__(self, identidad):
        """ Hace una consulta de un ciudadano """

        self._identidad = identidad
        self.recibo = 'N/D'
        self.nombre = 'N/D'
        self.municipio = 'N/D'
        self.inconcistencias = 'N/D'

        if len(identidad) == 13:
            # Obtener la página inicial para la consulta.
            while True:
                if self._navegador.open(self._url).status_code == 200:
                    break

            # Envía los datos al servidor hasta tener respuesta.
            while True:
                self._enviar_datos()
                error = self._navegador.get_current_page().select_one('header#titulerr')

                if not error:
                    break

            self.encontrado = self.encontrar_ciudadano()
        else:
            self.encontrado = False

    def encontrar_ciudadano(self):

        pagina_actual = self._navegador.get_current_page()
        elemento = pagina_actual.select_one('tr[id]')
        encontrado = bool(elemento)

        if encontrado:
            datos = elemento.findChildren('td', recursive=False)

            self.recibo = elemento['id']
            self.nombre = datos[1].string
            self.identidad = datos[2].string
            self.municipio = datos[3].string
            self.inconcistencias = int(datos[4].string)
        else:
            self.identidad = poner_guiones(self._identidad)

        return encontrado

    def _enviar_datos(self):
        """ Obtiene el código de verificación y envía las identidades """

        pagina = self._navegador.get_current_page()

        # Obteniendo codigo RNP
        img_encode = pagina.select_one('img.cod_rnp')['src'][23:]
        img_decode = b64decode(img_encode)
        img = Image.open(BytesIO(img_decode))
        cod_rnp = pytesseract.image_to_string(img)[:9]        

        # Enviando datos al servidor
        self._navegador.select_form('form[name=frmconsult]')
        self._navegador['identidad'] = self._identidad
        self._navegador['codigo'] = cod_rnp

        return self._navegador.submit_selected()

# Programa de línea de comandos.
if __name__ == '__main__':
    argumentos = sys.argv

    #try:
    with open(argumentos[1], 'r') as archivo_identidades:
        identidades = archivo_identidades.readlines()
        i = 1
        for identidad in identidades:
            identidad = identidad[:-1]
            print(f'Buscando la identidad «{identidad}»...')
            consulta = ConsultaIdentidad(identidad)

            if consulta.encontrado:
                print(f'Identidad encontrada a nombre de {consulta.nombre}')
                with open('IdentidadesConsultadas.csv', 'a') as respuesta:
                    respuesta.write(f'{i};{consulta.identidad};{consulta.nombre};{consulta.municipio}\n')
            else:
                print('Identidad no encontrada')
                with open('no-encontrados.csv', 'w') as no_encontrados:
                    no_encontrados.write(identidad + '\n')

            i += 1
    #except FileNotFoundError:
        #print('El Fichero no existe o no es el esperado')
    #finally:
        #print('Proceso terminado, saliendo...')
        #sys.exit()
