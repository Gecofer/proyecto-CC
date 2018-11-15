# ---------------------------------- util.py --------------------------------- #

# Autora: Gema Correa Fernández

# https://code.i-harness.com/en/q/ae54f
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


import unittest
from util import *

class myTest(unittest.TestCase):

    # ---------------------------------------------------------------------------- #
    # Función que devuelve todos los valores de la variable "data_twitter"
    def test_get_data_twitter(self):
        self.assertTrue(get_data_twitter(), "La lista está vacía")
    # ---------------------------------------------------------------------------- #
    # Función que devuelve uno de los valores de la variable "data_twitter"
    def test_get_id_data_twitter(self):
        self.assertIsInstance(get_id_data_twitter("VLC"), list, "No es una lista")
    # ---------------------------------------------------------------------------- #
    # Función que modificar uno de los atributos de la variable "data_twitter"
    #def test_update_data(self):
    #    user = "@UGR"
    #    update_data_twitter("VLC", "Valencia", user)
    #    update_data_twitter("VLC", "Madrid", user)
    #    self.assertTrue("Madrid" in get_names("VLC"), list, "No se ha añadido")

    def test_get_names(self):
        self.assertIsInstance(get_names("VLC"), dict, "No es un diccionario")
    # ---------------------------------------------------------------------------- #
    def test_remove_data_twitter(self):
        remove_data_twitter("VLC")
        self.assertTrue("VLC" not in get_data_twitter(), "No se ha borrado la lista")
    # ---------------------------------------------------------------------------- #
    def test_add_data_twitter(self):
        new_data = {"G": [{ "name":"@hol",
                     "url_twitter":"https://twitter.com/aytog",
                     "user_twitter":"@y"
                    }]}
        add_data_twitter(new_data)
        self.assertTrue(get_data_twitter(), "No se ha añadido la lista")
    # ---------------------------------------------------------------------------- #
    def test_get_names(self):
        self.assertIsInstance(get_names("VLC"), dict, "No es un diccionario")



if __name__ == '__main__':
    unittest.main()
