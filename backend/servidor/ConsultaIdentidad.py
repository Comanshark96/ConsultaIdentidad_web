import sys
import re
from io import BytesIO
from base64 import b64decode
import mechanicalsoup
import pytesseract
from PIL import Image


DNI_REGEX = r'^[10]{1}[0-9]{3}[1-9]{1}[0-9]{3}[0-9]{5}$'
DNI_GUION_REGEX = r'^[10]{1}[0-9]{3}-[1-9]{1}[0-9]{3}-[0-9]{5}$'

class ConsultaIdentidad:
    """ Consulta la identidad de un ciudadano en la base de datos del RNP.
    """

    _navegador = mechanicalsoup.StatefulBrowser()
    _url = 'http://www.rnp.hn/estadEnrolamiento/consulta_por_identidad'

    def __init__(self, identidad):
        """ Hace una consulta de un ciudadano """

        # Quitar guiones si este contiene el formato xxxx-xxxx-xxxxx
        if re.search(DNI_GUION_REGEX, identidad) is not None:
            identidad = identidad.replace('-', '')

        self.identidad = identidad
        self.recibo = 'N/D'
        self.nombre = 'N/D'
        self.lugar = 'N/D'
        self.inconcistencias = 'N/D'

        if re.search(DNI_REGEX, identidad) is not None:
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

            self.recibo = elemento['id'] # Elemento guardado en el id de la tabla.
            self.nombre = datos[1].string
            self.lugar = datos[3].string
            self.inconcistencias = int(datos[4].string)

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
        self._navegador['identidad'] = self.identidad
        self._navegador['codigo'] = cod_rnp

        return self._navegador.submit_selected()
