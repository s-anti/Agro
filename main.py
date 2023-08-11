from db import Db
from menu import Menu
import curses


nuleables = [
    "id_anim",
    "id_padre",
    "id_cli",
    "id_campo",
    "id_pot",
    "id_camp",
    "id_parc",
    # "car_animal",
    # "vol_pasto_l",
    # "vol_pasto_n",
    "observaciones",
    "fec_estimada",
    "estado_desc",
]
# Que valores pueden ser ingresados como nulos,
# Ya sea por que se autogeneran, como la foreign key,
# o por que no son estrictamente requeridos
# Se usa en ingresar()

fechas = ["fec_nac", "fec_alta", "fec_estimada"]
decimales = [
    "peso_nac",
    "hectareas",
    "ancho",
    "largo",
    "car_animal",
    "vol_pasto_l",
    "vol_pasto_n",
]

rangos = {
    "cat": ["Vaquillona", "Ternera", "Vaca adulta"],
    "sub_cat": ["Primera parición", "Segunda parición", "Vaca descarte"],
    "tipo_campo": ["Sierra", "Llano"],
    "hembra": ["Macho", "Hembra"],
}
textos = [
    "nombre",
    "apellido",
    "telefono",
    "email",
    "propietario",
    "observaciones",
    "estado_desc",
]


def ingresar(paraQue, variable):
    print("")
    print("Ingrese el valor para", paraQue)

    if variable in nuleables:
        print("Presione 'enter' si no tiene (Se puede modificar)")

    elif variable in rangos.keys():
        print("Las opciones son:")
        for i, j in enumerate(rangos[variable]):
            print(f"{i + 1}) {j}")

        while True:
            valor = input("Valor: ")

            if valor.isnumeric():
                valor = int(valor)

                if valor - 1 in range(len(rangos[variable])):
                    return valor

            print(f"Ingrese un entero del 1 al {len(rangos[variable])}...")

    print("Ingrese 0 para cancelar la operación")

    while True:
        valor = input("Valor: ")

        if valor.lower().strip() == "" and variable in nuleables:
            return

        if valor.lower().strip() == "0":
            return "CANCELAMOS"

        else:
            if variable in fechas:
                print("FORMATEO DE FECHAS MASTER")
                return valor

            elif variable in decimales:
                try:
                    valor = float(valor)
                    if valor > 0:
                        return valor
                    else:
                        print("Ingrese un número positivo...")
                except ValueError:
                    print("Ingrese un número válido...")

            elif variable in textos:
                return valor

            else:
                if valor.isnumeric():
                    return int(valor)

                else:
                    print("Ingrese un entero positivo")


def cargar(datos, textos):
    # len datos debe corresponder con len textos
    # los datos a cargar son como va en el registro
    # Textos es visual

    diccionario = {}
    for llave, texto in zip(datos, textos):
        c = ingresar(texto, llave)
        if c == "CANCELAMOS":
            return
        diccionario[llave] = c

    print("Sacamso", diccionario)
    return diccionario


class Main:
    def cargarVaca(self):
        valores = cargar(
            [
                "id_anim",
                "id_padre",
                "id_madre",
                "fec_nac",
                "peso_nac",
                "hembra",
                "cat",
                "sub_cat",
            ],
            [
                "el código de la vaca (Opcional)",
                "el código del padre (Opcional)",
                "el código de la madre",
                "la fecha de nacimiento",
                "el peso al nacer",
                "saber si es macho o hembra",
                "su categoría",
                "su subcategoría",
            ],
        )

        if valores:
            self.cargar("animal", [*valores.values()])
        else:
            print("Se canceló la operación")

    def cargarCampo(self):
        valores = cargar(
            [
                "id_camp",
                "fec_alta",
                "tipo_campo",
                "nombre",
                "propietario",
                "telefono",
                "email",
                "hectareas",
            ],
            [
                "el código del campo (Opcional)",
                "la fecha de inicio de producción",
                "el tipo de campo",
                "el nombre del campo",
                "el propietario",
                "el telefono asociado",
                "el e-mail asociado",
                "la cantidad de hectáreas",
            ],
        )

        if valores:
            self.cargar("campo", [*valores.values()])

    def cargarPotrero(self):
        valores = cargar(
            [
                "id_pot",
                "id_camp_pot",
                "ancho",
                "largo",
                "car_animal",
                "vol_pasto_n",
                "vol_pasto_l",
            ],
            [
                "el código del potrero (Opcional)",
                "el campo donde está el potrero",
                "el ancho del potrero, en m",
                "el largo del potrero, en m",
                "la carga animal",
                "el volúmen de pasto N",
                "el volúmen de pasto L",
            ],
        )

        if valores:
            self.cargar("potrero", [*valores.values()])

    def cargarParcela(self):
        valores = cargar(
            ["id_parc", "id_pot_parc", "observaciones"],
            [
                "el código de la parcela (opcional)",
                "el potrero donde está",
                "otras observaciones (opcional)",
            ],
        )

        if valores:
            self.cargar("parcela", [*valores.values()])

    def __init__(self, seEjectua=True) -> None:
        self.db = Db()

        # Mostrar vacas por parcelas, campos y potreros
        # Ver cantidad máxima de vacas por parcela, campo y potrero
        # Listado de campos
        # Listado de parcelas
        # Listado de animales

        dicc = {
            "Proyecto ingeniero agrónomo": {
                "Menu animales": {
                    "Listar animales": {
                        "Por campo": lambda: print("Mostrando por campo"),
                        "Por potrero": lambda: print("Mostrando por potrero"),
                        "Por parcela": lambda: print("Mostrando por parcela"),
                        "Todos": lambda: print("Mostrando odos"),
                    },
                    "Cargar animal": self.cargarVaca,
                    "Modificar animal": lambda: print("Modificando un animal"),
                    "Cargar seguimiento": lambda: print(
                        "Cargando el seguimiento de la vaca"
                    ),
                    "Eliminar animal": lambda: print("Eliminando un animal"),
                },
                "Campos, potreros y parcelas": {
                    "Campos": {
                        "Listar Campos": lambda: print("Listando Campos"),
                        "Cargar Campos": self.cargarCampo,
                        "Modificar Campos": lambda: print("Modificando Campos"),
                        "Eliminar Campos": lambda: print("Eliminando Campos"),
                    },
                    "Potreros": {
                        "Listar Potreros": lambda: print("Listando Potreros"),
                        "Cargar Potreros": self.cargarPotrero,
                        "Modificar Potreros": lambda: print("Modificando Potreros"),
                        "Eliminar Potreros": lambda: print("Eliminando Potreros"),
                    },
                    "Parcelas": {
                        "Listar Parcelas": lambda: print("Listando Parcelas"),
                        "Cargar Parcelas": self.cargarParcela,
                        "Modificar Parcelas": lambda: print("Modificando Parcelas"),
                        "Eliminar Parcelas": lambda: print("Eliminando Parcelas"),
                    },
                },
                "usuario": {
                    "listado usuarios": lambda: print("Listado de usuarios"),
                    "carga de usuarios": lambda: print("Carga de usuarios"),
                    " de usuarios": lambda: print(" de usuarios"),
                    "carga de usuarios": lambda: print("Carga de usuarios"),
                },
            }
        }

        self.menu = Menu(dicc)

        if seEjectua:
            self.menu.iniciar()

    def cargar(self, tabla: str, datos: list) -> None:
        signos = ("?, " * (len(datos) - 1)) + "?"
        # Crea un string "(?, ?, ?)" con la cantidad de signos necesitada por la consulta

        print(
            "El string para el query en cargar es ",
            "insert into {} values ({})".format(tabla, signos),
        )
        print("con", datos)
        self.db.insert("insert into {} values ({})".format(tabla, signos), datos)
        pass


main = Main(False)
main.menu.iniciar()
