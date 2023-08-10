from db import Db
from menu import Menu

a = Db()
estructura = {
    "animal": {
        "o seguimiento": lambda: print("Cargar el seguimiento de la vaca"),
        "o informe": lambda: print("Ver seguimientos previos de la vaca"),
        "o consultas": lambda: print("Ver información de todas las vacas"),
    },
    "campos": {
        "consultas": {
            "cambio parcelas": lambda: print("Cambio de parcelas"),
            "cambio potrero": lambda: print("Cambio de potrero"),
            "cambio campo": lambda: print("Cambio de campo"),
        },
        "listado potreros": lambda: print("Listado de potreros"),
        "carga de potreros": lambda: print("Carga de potreros"),
        "modificacion de potreros": lambda: print("Modificación de potreros"),
        "baja de potreros": lambda: print("Baja de potreros"),
    },
    "usuario": {
        "listado usuarios": lambda: print("Listado de usuarios"),
        "carga de usuarios": lambda: print("Carga de usuarios"),
        "modificacion de usuarios": lambda: print("Modificación de usuarios"),
        "baja de usuarios": lambda: print("Baja de usuarios"),
    },
}

menu = Menu(estructura)
menu.iniciar()
