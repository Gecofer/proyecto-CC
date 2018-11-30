# Extrayendo datos de Twitter

Para el desarollo de mi proyecto, necesito la obtención de datos geolocalizados a partir de _trending topics_ o tendencias. Por lo tanto, vamos a obtener las tendencias para una región determinada. Para ello, debemos hacer uso de la API de Twitter, la cual nos permite acceder a toda esa información. A continuación, se muestran algunos de los datos que podemos extraer [[1][1]]:

- **Tweets**: búsqueda, publicación, filtrado, etc.
- **Anuncios**: gestión de campañas, análisis, etc.
- **Contenido multimedia**: subir y acceder a fotos, vídeos, GIF animados, etc.
- **Tendencias**: trending topics.
- **Geo**: información sobre lugares conocidos, lugares cerca de una ubicación, etc.

### Bibliotecas de Python para la API de Twitter

Python cuenta con muchas bibliotecas desarrolladas para la API de Twitter. Sin embargo, al no haber usado nunca ninguna me es dífil elegir que biblioteca es la mejor. Es por ello, que voy hacer uso de [tweepy](https://github.com/tweepy/tweepy) ya que he oído hablar de ella bastante bien y tiene bastante documetación en la web. De todas maneras, existen otras librerías cómo [twython](https://github.com/ryanmcgrath/twython), [python-twitter](https://github.com/bear/python-twitter) o [TwitterAPI](https://github.com/geduldig/TwitterAPI).

### API REST de Twitter y Tweepy

Twitter ofrece una API muy fácil de usar que nos permite extraer una gran cantidad de información útil sobre un usuario[[2][2]]. Para extraer todo este tipo de información, vamos hacer uso de la librería para Python llamada Tweepy, la cual nos permite manejar la API desde Python de una forma muy cómoda y sencilla. Para instalar esta librería, podemos instalarla gracias a `pip` de la siguiente manera:

~~~
pip install tweepy
~~~

Una vez instalado, ya podremos empezar a trabajar con Twitter y Python.








https://github.com/lauramayol/laura_python_core/blob/b0f62fb70ecef0e8f3d5e8476665a48519dfc44e/week_05/mini_projects/api_from_other_apis/tweet.py

[1]: https://stackabuse.com/accessing-the-twitter-api-with-python/
[2]: https://geekandtechgirls.github.io/The-Spyder-Girl/project/2017/03/11/extrayendo-datos-twitter.html
