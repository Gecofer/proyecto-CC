# -------------------------------- app_test.py ------------------------------- #

# Autora: Gema Correa Fernández

'''
Fichero que testea main.py
'''

# https://code.i-harness.com/en/q/ae54f
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Bibliotecas a usar
import unittest     # https://docs.python.org/3/library/unittest.html
# https://www.blog.pythonlibrary.org/2016/07/07/python-3-testing-an-intro-to-unittest/
#import requests     # https://www.pythonforbeginners.com/requests/using-requests-in-python
import main
import json
from data import *

# https://stackoverflow.com/questions/20309456/call-a-function-from-another-file-in-python


class TestTwitterData(unittest.TestCase):

# ---------------------------------------------------------------------------- #

    # Si el método setUp() hace una excepción mientras se ejecuta la prueba,
    # el framework considerará que la prueba ha sufrido un error y el método
    # de prueba no se ejecutará.
    def setUp(self):
        # self.twitter_data = TwitterData()
        # Creamos el cliente que se va a utilizar.
        self.app = main.app.test_client()

 # --------------------------------------------------------------------------

    # Para comprobar Flask
    def test0_app_run(self):
        self.assertEqual(main.app.debug, False, "Comprobar app run")

        pass

# ---------------------------------------------------------------------------- #

    # Testear que se ha desplegado correctamente
    def test1_index(self):
        # result = requests.get('http://127.0.0.1:5000/')
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")

        pass

# ---------------------------------------------------------------------------- #

    # Testear que se ha desplegado correctamente
    def test2_error(self):
        #result = requests.get('http://127.0.0.1:5000/')
        result = self.app.get("/data")
        self.assertEqual(result.status_code, 404)

        pass

# ---------------------------------------------------------------------------- #

    # Testear que se visualizan todos los elementos
    def test3_get_all_data(self):
        #result = requests.get('http://127.0.0.1:5000/data_twitter')
        result = self.app.get("/data_twitter")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        self.assertTrue(result.get_json(), "The list is empty")

        pass

# ---------------------------------------------------------------------------- #

    # Testear que se visualiza uno de los elementos
    def test4_get_data(self):
        #result = requests.get('http://127.0.0.1:5000/get_data?id=GR')
        result = self.app.get("/data_twitter/Rudy")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        self.assertTrue(result.get_json(), "The list is empty")

        # Escribimos la ruta mal
        result_bad = self.app.get("/hola")
        self.assertEqual(result_bad.status_code, 404)

        pass


# ---------------------------------------------------------------------------- #

    # Testear que se crea un elemento
    def test5_put_data(self):
        new_data = {
                    "name": "hola",
                    "url": "hola.es",
                    "query": "hola",
                    "tweet_volume": "1234567"
                    }

        #result_put = requests.put('http://localhost:5000/data_twitter', data=new_data)
        result = self.app.put("/data_twitter")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        self.assertTrue(result.get_json(), "The list is empty")

        pass

# ---------------------------------------------------------------------------- #

    # Testear que se modifica un elemento
    def test6_post_data(self):
        #result_post = requests.post('http://127.0.0.1:5000/data_twitter?id=GR')
        result = self.app.post("/data_twitter/Bernabeu")
        #result = requests.post('http://127.0.0.1:5000/data_twitter_update?name=name&user=hola&id=GR')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        #add_data_twitter("Canarias")
        self.assertTrue(result.get_json(), "The list is empty")

        pass


# ---------------------------------------------------------------------------- #

    # Testear que se elimina un elemento
    def test7_delete_data(self):

        #result_delete = requests.delete('http://127.0.0.1:5000/data_twitter?id=VLC')
        result_delete = self.app.delete("/data_twitter/hola")
        self.assertEqual(result_delete.status_code, 200)
        self.assertEqual(result_delete.content_type, "application/json")
        self.assertTrue(result_delete.get_json(), "The list is empty")

        result_post1 = self.app.post("/data_twitter/#GHVIPGala12")
        result_delete1 = self.app.delete("/delete_data/#GHVIPGala12")
        result_post2 = self.app.post("/data_twitter/#GHVIPGala12")
        self.assertEqual(result_post2.status_code, 404)

        pass


# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
