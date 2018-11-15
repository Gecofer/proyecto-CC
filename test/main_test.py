# -------------------------------- app_test.py ------------------------------- #

# Autora: Gema Correa Fernández

'''
Fichero que testea la clase de app.py
'''

# https://code.i-harness.com/en/q/ae54f
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Bibliotecas a usar
import unittest     # https://docs.python.org/3/library/unittest.html
# https://www.blog.pythonlibrary.org/2016/07/07/python-3-testing-an-intro-to-unittest/
import requests     # https://www.pythonforbeginners.com/requests/using-requests-in-python



# https://stackoverflow.com/questions/20309456/call-a-function-from-another-file-in-python

import main
from util import *


class TestTwitterData(unittest.TestCase):

# ---------------------------------------------------------------------------- #

    # Si el método setUp() hace una excepción mientras se ejecuta la prueba,
    # el framework considerará que la prueba ha sufrido un error y el método
    # de prueba no se ejecutará.
    def setUp(self):
        # self.twitter_data = TwitterData()
        # Creamos el cliente que se va a utilizar.
        self.app = main.app.test_client()

# ---------------------------------------------------------------------------- #

    # Testear que se ha desplegado correctamente
    def test_index(self):
        # result = requests.get('http://127.0.0.1:5000/')
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")
        pass


# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #

    # Testear que se visualiza uno de los elementos
    def test_get_data(self):
        result = requests.get('http://127.0.0.1:5000/get_data?id=GR')
        #result = self.app.get("/get_data?id=GR")
        self.assertEqual(result.status_code, 200)
        #self.assertEqual(result.content_type, "application/json")
        #self.assertIsInstance(get_id_data_twitter("VLC"), list, "It's not a list")


        # Escribimos la ruta mal
        result_bad = self.app.get("/hola")
        self.assertEqual(result_bad.status_code, 404)

        pass

# ---------------------------------------------------------------------------- #

    # Testear que se visualizan todos los elementos
    def test_get_all_data(self):

        ## GET
        result_get = requests.get('http://localhost:5000/data_twitter')
        #result_get = self.app.get("/data_twitter")
        self.assertEqual(result_get.status_code, 200)
        #self.assertEqual(result_get.content_type, "application/json")
        self.assertTrue(get_data_twitter(), "The list is empty")
        pass

# ---------------------------------------------------------------------------- #
    def test_put_data(self):

        ## PUT
        new_data = {"G": [{ "name":"@hol",
                         "url_twitter":"https://twitter.com/aytog",
                         "user_twitter":"@y"
                        }]}

        result_put = requests.put('http://localhost:5000/data_twitter', data=new_data)
        #result_put = self.app.put("/data_twitter")
        self.assertEqual(result_put.status_code, 200)
        #self.assertEqual(result_put.content_type, "application/json")
        add_data_twitter(new_data)
        self.assertTrue(get_data_twitter(), "No se ha añadido la lista")
        pass

# ---------------------------------------------------------------------------- #

    def test_post_data(self):

        ## POST
        result_post = requests.post('http://127.0.0.1:5000/data_twitter?id=GR')
        #result_post = self.app.post("/data_twitter?id=GR")
        #result = requests.post('http://127.0.0.1:5000/data_twitter_update?name=name&user=hola&id=GR')
        self.assertEqual(result_post.status_code, 200)
        # self.assertEqual(result_post.content_type, "application/json")
        #add_data_twitter("Canarias")
        update_data_twitter("MDR", "name", "Canarias")
        get_id_data_twitter("MDR")
        self.assertIn("MDR",get_data_twitter())
        #self.assertTrue("GR" in get_data_twitter(), "No se ha añadido la lista")


# ---------------------------------------------------------------------------- #

    def test_delete_data(self):
        ## DELETE
        result_delete = requests.delete('http://127.0.0.1:5000/data_twitter?id=VLC')
        #result_delete = self.app.delete("/data_twitter?id=VLC")
        self.assertEqual(result_delete.status_code, 200)
        #self.assertEqual(result_delete.content_type, "application/json")
        remove_data_twitter("GR")
        #self.assertTrue("GR" not in get_data_twitter(), "No se ha eliminado la lista")
        self.assertNotIn("GR",get_data_twitter())

        result_post1 = self.app.post("/data_twitter?id=GR")
        result_delete1 = self.app.delete("/delete_data?id=GR")
        result_post2 = self.app.post("/data_twitter?id=GR")
        self.assertEqual(result_post2.status_code, 200)

        pass


# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    unittest.main()
