# ---------------------------------- util.py --------------------------------- #

# Autora: Gema Correa Fernández

'''
Fichero que contiene la información a mostrar en la clase TwitterData
'''

# ---------------------------------------------------------------------------- #
# Nos creamos los datos (tipo JSON)

data_twitter = {
    "GR": [
            {
                "name":"Granada",
                "url_twitter":"https://twitter.com/aytogr?lang=es",
                "user_twitter":"@aytogr"
            },
        ]
    ,

    "MDR": [
            {
                "name":"Madrid",
                "url_twitter":"https://twitter.com/madrid",
                "user_twitter":"@MADRID"
            },
        ]
    ,

    "VLC": [
            {
                "name":"Valencia",
                "url_twitter":"https://twitter.com/ajuntamentvlc?lang=es",
                "user_twitter":"@AjuntamentVLC",
            },
        ]
}


# ---------------------------------------------------------------------------- #
# Función que devuelve todos los valores de la variable "data_twitter"
def get_data_twitter():
    return data_twitter
# ---------------------------------------------------------------------------- #
# Función que devuelve uno de los valores de la variable "data_twitter"
def get_id_data_twitter(data):
    if data in data_twitter:
        return data_twitter[data]
    else:
        return False
# ---------------------------------------------------------------------------- #
# Función que modificar uno de los atributos de la variable "data_twitter"
def update_data_twitter(data, name, user):
    if data in data_twitter:
        data_twitter[data][0][name] = user
        return True
    else:
        return False
# ---------------------------------------------------------------------------- #
def remove_data_twitter(data):
    if data in data_twitter:
        del data_twitter[data]
        return True
    else:
        return False
# ---------------------------------------------------------------------------- #
def add_data_twitter(new_data):
    new_data_twitter = data_twitter
    new = new_data_twitter.update(new_data)
    return new
# ---------------------------------------------------------------------------- #
def get_names(data):
    if data in data_twitter:
        return data_twitter[data][0]
    else:
        return False
# ---------------------------------------------------------------------------- #
def get_user(data, name):
    if data in data_twitter:
        return data_twitter[data][0][name]
    else:
        return False
# ---------------------------------------------------------------------------- #










































'''
def get_id_data_twitter(data):
    if data in data_twitter:
        return data_twitter[data]
    else:
        return False

def update_data_twitter(data, name, user):
    if data in data_twitter:
        data_twitter[data][0][name] = user
        return True
    else:
        return False

def get_names(data):
    if data in data_twitter:
        return data_twitter[data][0]
    else:
        return False


#def get_user(data, name):
#    if data in data_twitter:
#        return data_twitter[data][0][name] # [0]
#    else:
#        return False
'''
