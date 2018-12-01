# Extrayendo datos de Twitter

Para el desarollo de mi proyecto, necesito la obtención de datos geolocalizados a partir de _trending topics_ o tendencias. Por lo tanto, vamos a obtener las tendencias para una región determinada, en este caso de Granada. Para ello, debemos hacer uso de la API de Twitter, la cual nos permite acceder a toda esa información. A continuación, se muestran algunos de los datos que podemos extraer [[1][1]]:

- **Tweets**: búsqueda, publicación, filtrado, etc.
- **Anuncios**: gestión de campañas, análisis, etc.
- **Contenido multimedia**: subir y acceder a fotos, vídeos, GIF animados, etc.
- **Tendencias**: trending topics.
- **Geo**: información sobre lugares conocidos, lugares cerca de una ubicación, etc.

### Bibliotecas de Python para la API de Twitter

Python cuenta con muchas bibliotecas desarrolladas para la API de Twitter. Sin embargo, al no haber usado nunca ninguna me es díficil elegir que biblioteca escoger. Es por ello, que voy hacer uso de [tweepy](https://github.com/tweepy/tweepy) ya que he oído hablar de ella bastante bien y tiene bastante documetación en la web. De todas maneras, existen otras librerías cómo [twython](https://github.com/ryanmcgrath/twython), [python-twitter](https://github.com/bear/python-twitter) o [TwitterAPI](https://github.com/geduldig/TwitterAPI).

### API REST de Twitter y Tweepy

Twitter ofrece una API muy fácil de usar que nos permite extraer una gran cantidad de información útil sobre un usuario [[2][2]]. Para extraer todo este tipo de información, vamos hacer uso de la librería para Python llamada Tweepy, la cual nos permite manejar la API desde Python de una forma muy cómoda y sencilla. Para instalar esta librería, podemos instalarla gracias a `pip` de la siguiente manera:

~~~
pip install tweepy
~~~

Una vez instalado, ya podremos empezar a trabajar con Twitter y Python. Para ello, lo primero que debemos hacer es obtener unas claves de acceso para Twitter. Esto se puede hacer accediendo a la página de [Twitter Aps](https://apps.twitter.com), creando una nueva app y obteniendo las claves siguientes:

- _Consumer Key (API Key)_
- _Consumer Secret Key (API Secret)_
- _Access Token_
- _Access Token Secret_

![](../docs/images/claves_twitter.png)

Para hacer un uso correcto de estas claves de acceso privadas, es aconsejable ponerlas como variables de entorno en nuestro bash, realizando un export [[3][3]].

~~~
auth = tweepy.OAuthHandler(environ["TWITTER_CONSUMER_KEY"],
                          environ["TWITTER_CONSUMER_SECRET"])

auth.set_access_token(environ["TWITTER_ACCESS_TOKEN"],
                      environ["TWITTER_ACCESS_TOKEN_SECRET"])
~~~

Una vez que ya tenemos acceso a la API, se realiza la función `API.trends_place(id[, exclude])` [[4][4]], que devuelve las 10 tendencias virales en formato JSON. (_Esta información se almacena en caché durante 5 minutos. Solicitar con frencuencia no devolverá más datos y contará en contra de su límite de uso, es por eso que es aconsejable ralizar pocas solicitudes y guardarlo en un archivo._)



[1]: https://stackabuse.com/accessing-the-twitter-api-with-python/
[2]: https://geekandtechgirls.github.io/The-Spyder-Girl/project/2017/03/11/extrayendo-datos-twitter.html
[3]: https://github.com/lauramayol/laura_python_core/blob/b0f62fb70ecef0e8f3d5e8476665a48519dfc44e/week_05/mini_projects/api_from_other_apis/tweet.py
[4]: http://docs.tweepy.org/en/v3.5.0/api.html

### Enlaces Interesantes

- [Acceso a la Twitter de API con Python](https://stackabuse.com/accessing-the-twitter-api-with-python/)
- [API Reference Tweepy](http://docs.tweepy.org/en/v3.5.0/api.html)
- [API REST de Twitter y Tweepy](https://geekandtechgirls.github.io/The-Spyder-Girl/project/2017/03/11/extrayendo-datos-twitter.html)
- [Ejemplo para obtener las tendencias de una localización con Tweepy](https://github.com/lauramayol/laura_python_core/blob/b0f62fb70ecef0e8f3d5e8476665a48519dfc44e/week_05/mini_projects/api_from_other_apis/tweet.py)
