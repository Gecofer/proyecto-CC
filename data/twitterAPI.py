# ------------------------------- twitterAPI.py ------------------------------ #

# Autora: Gema Correa Fernández

'''
Fichero que accede a la API de Twitter y obtiene los 5 trending topic de una
ubicación determinada, en nuestro caso, de la provincia de Granada
'''

# Librerías a importar
import tweepy  # Para acceder a la API de Twitter (http://docs.tweepy.org/en/v3.5.0/api.html)
import os      # Para acceder a funcionalidades dependientes del SO (entorno)

from pprint import pprint   # Para imprimir estructuras de datos arbitrarias
from os import environ      # Para obtener las variables de entorno

# Para situarnos en el directorio raíz
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Para hacer uso de logs
import logging
logger = logging.getLogger("data")
logging.basicConfig(filename= "../debug.log", filemode='a', format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

class Trends:

    '''
    Función que nos permite conectarnos con la API de Twitter para poder extraer datos
    '''
    def twitter_connection(self):

        # Definimos las claves como variables de entorno en nuestro bash mediante un export
        auth = tweepy.OAuthHandler(environ["TWITTER_CONSUMER_KEY"],
                                   environ["TWITTER_CONSUMER_SECRET"])

        auth.set_access_token(environ["TWITTER_ACCESS_TOKEN"],
                              environ["TWITTER_ACCESS_TOKEN_SECRET"])

        return tweepy.API(auth)

    '''
    Función que obtiene los trending topics de una ubicación determinada

    - api (object) = conexión con Twitter mediante la librería Tweepy API
    - lat (float) = latitud de la localización a buscar
    - long (float) = longitud de la localización a buscar

    - Devuelve los 5 trending topics de Twitter de la localización más cercana
    '''
    def get_location_trends(self, api, lat, long):

        # Consigue la primera ubicación más cercana en Twitter basada en (lat, long)
        # Tweepy ya ordena por lo más cercano
        locations = api.trends_closest(lat, long)
        for i in range(1):
            twitter_location = locations[i]

        # Obtener las 5 mejores tendencias de acuerdo a twitter_location
        # Ordenadas por tweet_volume (máximo primero)
        top_trends = api.trends_place(twitter_location['woeid'])[0]['trends']
        top_trends = sorted(top_trends, key=lambda dict: dict['tweet_volume'] or 0, reverse=True)

        return top_trends[:5]


if __name__ == '__main__':

    # Obtener las tendencias de las ubicaciones más cercanas en Twitter
    my_trend = Trends()
    my_api = my_trend.twitter_connection()
    logger.info("Successfully connected API Twitter.")

    # Defino para Granada su latitud y longitud
    print(my_trend.get_location_trends(my_api, 37.1833, -3.6))
    logger.info("Successfully obtain location trends.")
