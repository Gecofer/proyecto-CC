# ----------------------------------- log.py ---------------------------------- #

# Con ayuda de:
# - https://ricveal.com/blog/curso-python-5/
# - https://docs.python.org/3.1/library/logging.html
# - http://lineadecodigo.com/python/logs-en-flask/

# Bibliotecas a usar
import logging  # http://flask.pocoo.org/docs/1.0/logging/

'''
Fichero que configura un único sistema de log y que maneja eventos de dos
formas diferentes: guardándolo en un archivo si la traza es de nivel DEBUG o
superior y/o sacándolo por pantalla en el mismo caso.
'''
def logger(name):

    # http://flask.pocoo.org/docs/0.12/errorhandling/
    # Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    log = logging.Logger(name)

    # FileHandler
    # Guardar los logs en el archivo debug.log
    filehandler = logging.FileHandler('debug.log')
    # si la traza es de nivel DEBUG o superior
    filehandler.setLevel(logging.DEBUG)

    # ConsoleHandler
    # Mostrar los logs por pantalla
    consolehandler = logging.StreamHandler()
    # si la traza es de nivel DEBUG o superior
    consolehandler.setLevel(logging.DEBUG)

    # Modificar el formato (http://flask.pocoo.org/docs/1.0/logging/)
    # Para que aparezca la fecha, el nombre de la app, el nivel del mensaje y el mensaje
    # format = logging.basicConfig(filemode='w', format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # tanto en el archivo
    filehandler.setFormatter(format)
    # como en la salida por pantalla o consola
    consolehandler.setFormatter(format)

    # Vamos añadiendo los logs (mensajes) tanto a la consola como al archivo
    log.addHandler(filehandler)
    log.addHandler(consolehandler)

    return log
