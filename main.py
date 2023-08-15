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
    "id_segui",
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
    "sexo": ["Macho", "Hembra"],
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

# def modificarVaca
# valores = modificar
# if valores self.modificar
diccTitulos = {
    "id_anim": "ID Animal",
    "id_padre": "ID Padre",
    "id_madre": "ID Madre",
    "fec_nac": "Nacimiento",
    "peso_nac": "Peso nacimiento",
    "sexo": "Sexo",
    "cat": "Categoría",
    "sub_cat": "Subcategoría",
    "parc": "Parcela",
    "id_camp": "ID Campo",
    "fec_alta": "Fecha de alta",
    "tipo_campo": "Tipo",
    "nombre": "Nombre",
    "propietario": "Propietario",
    "telefono": "Teléfono",
    "email": "E-Mail",
    "hectareas": "Hectáreas",
    "id_pot": "ID Potrero",
    "id_camp_pot": "ID Campo",
    "ancho": "Ancho",
    "largo": "Largo",
    "car_animal": "Carga animal",
    "vol_pasto_n": "Volumen pasto N",
    "vol_pasto_l": "Volumen pasto L",
    "id_parc": "ID Parcela",
    "id_pot_parc": "ID Potrero",
    "observaciones": "Observaciones",
    "id_cli": "ID Cliente",
    "apellido": "Apellido",
}


def ingresar(paraQue, variable, datoViejo=None):
    # TODO: VALIDAR UNIQUES
    print("")
    print("Ingrese el valor para", paraQue)

    if variable in nuleables and not datoViejo:
        print("Presione 'enter' si no tiene (Se puede modificar)")

    if datoViejo:
        if variable in rangos:
            print(
                f"Presione 'enter' para mantener el valor '{rangos[variable][int(datoViejo)]}'"
            )
        else:
            print(f"Presione 'enter' para mantener el valor '{datoViejo}'")

    print("Ingrese 0 para cancelar la operación")

    if variable in rangos.keys():
        print("Las opciones son:")
        for i, j in enumerate(rangos[variable]):
            print(f"{i + 1}) {j}")

    while True:
        valor = input("Valor: ")

        if valor.lower().strip() == "":
            if datoViejo:
                return datoViejo
                # Se debería poder nulear un dato ya ingbersado pero ya fue
            if variable in nuleables:
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

            elif variable in rangos:
                if valor.isnumeric():
                    valor = int(valor)

                    if valor - 1 in range(len(rangos[variable])):
                        return valor

                print(f"Ingrese un entero del 1 al {len(rangos[variable])}...")

            else:
                if valor.isnumeric():
                    return int(valor)

                else:
                    print("Ingrese un entero positivo")


# Funciones de apoyo
def cargar(datos, textos, datos_viejos=None):
    # len datos debe corresponder con len textos
    # los datos a cargar son como va en el registro
    # Textos es visual

    indice = 0
    diccionario = {}
    for llave, texto in zip(datos, textos):
        # Le paso los datos viejos si estamos modificando, si no, no
        c = ingresar(texto, llave, datos_viejos[indice] if datos_viejos else None)
        if c == "CANCELAMOS":
            return
        diccionario[llave] = c
        indice += 1

    # Confirmación
    print("\nDatos cargados: ")
    # tabla() si o sí me pide una lista de diccionarios así que tiene que ir así

    for key, value in diccionario.items():
        print(f"{diccTitulos[key]}: {value}")
    print("")
    while True:
        print("Confirma estos datos?")
        v = input("Si, No: ").lower().strip()

        if v in ("si", "s", "1"):
            return diccionario
        elif v in ("no", "n", 0):
            return

        print("No valido, reintente...")


def tabla(datos):
    print("Datos sobn", datos)

    if not datos:
        print("No hay registros para mostrar")
        return
    anchos = []
    header = ""

    for dato in datos[0].keys():
        dt = f"   {diccTitulos[dato]}   "

        anchos.append(len(dt))

        header += dt

    print(header)

    for linea in datos:
        lineaTexto = ""
        keys = [*linea.keys()]

        for i, dato in enumerate(linea):
            # Si la key está dentro de los rangos, en vez del dato presento el valor asociado
            # Se puede expandir para otros tipos de dato
            # print(f"dato {dato} i {i} keys[i] {keys[i]}")
            # if keys[i] in rangos:
            #     lineaTexto += str(rangos[keys[i]][int(dato) - 1]).center(anchos[i])
            # else:
            lineaTexto += str(dato).center(anchos[i])

        print(lineaTexto)


class Main:
    def validarEnTabla(self, tabla, idN):
        print("Ingrese la ID para modificar")
        print("Ingrese 0 para cancelar")
        while True:
            valor = input("Valor: ")

            valor = valor.strip()

            if valor.isnumeric():
                if int(valor) == 0:
                    return
                elif int(valor) > 0:
                    r = self.leer(
                        "select * from {} where {} = {}".format(tabla, idN, valor)
                    )

                    if r:
                        return valor
                    else:
                        print("No se encuentra")
                else:
                    print("Ingrese un positivo")
            else:
                print("Ingrese un número...")

    def cargarVaca(self):
        valores = cargar(
            [
                "id_anim",
                "id_padre",
                "id_madre",
                "fec_nac",
                "peso_nac",
                "sexo",
                "cat",
                "sub_cat",
                "parc",
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
                "la parcela donde está",
            ],
        )

        if valores:
            self.cargar("animal", [*valores.values()])
        else:
            print("Se canceló la operación")

    def modificarVaca(self):
        # TODO: ver que hago con esto, que se puede modificar
        idObj = self.validarEnTabla("animal", "id_anim")

        datos = cargar(
            [
                "id_padre",
                "id_madre",
                "fec_nac",
                "peso_nac",
                "sexo",
                "cat",
                "sub_cat",
                "parc",
            ],
            [
                "la nueva ID del padre",
                "la nueva ID de la madre",
                "la nueva fecha de nacimiento",
                "el nuevo peso de nacimiento",
                "el nuevo sexo",
                "la nueva categoría",
                "la nueva subcategoría",
                "la nueva parcela",
            ],
            self.leer(
                "select id_padre, id_madre, fec_nac, peso_nac, sexo, cat, sub_cat, parc from animal where id_anim = {}".format(
                    idObj
                )
            )[0],
        )

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

    def cargarSeguimiento(self):
        valores = cargar(
            ["id_segui", "id_anim_seg", "estado_desc", "fec_estimada"],
            [
                "el código de seguimiento (opcional)",
                "el código del animal",
                "la descripción",
                "la fecha estimada de nacimiento",
            ],
        )

        if valores:
            self.cargar("seguimiento", [*valores.values()])

    def leerVacasTodos(self):
        tabla(self.leer("select * from animal"))

    def leerVacasCampo(self):
        campo = input("Ingrese el campo para buscar: ")
        tabla(
            self.leer(
                """select animal.* from animal
        join parcela on id_parc = parc
        join potrero on id_pot = id_pot_parc
        join campo on id_camp = id_camp_pot
        where id_camp = {}""".format(
                    campo
                )
            )
        )

    def leerVacasPotrero(self):
        pot = input("Ingrese el potrero para buscar: ")
        tabla(
            self.leer(
                """select animal.* from animal
        join parcela on id_parc = parc
        join potrero on id_pot = id_pot_parc
        where id_pot = {}""".format(
                    pot
                )
            )
        )

    def leerVacasParcela(self):
        parcela = input("Ingrese la parcela para buscar: ")
        tabla(
            self.leer(
                """select animal.* from animal
        join parcela on id_parc = parc
        join potrero on id_pot = id_pot_parc
        where id_pot = {}""".format(
                    parcela
                )
            )
        )

    def leerCampos(self):
        tabla(self.leer("select * from campo"))

    def leerPotreros(self):
        tabla(self.leer("select * from potrero"))

    def leerParcelas(self):
        tabla(
            self.leer(
                """select parcela.*, id_camp from parcela join potrero on id_pot = id_pot_parc join campo on id_camp = id_camp_pot"""
            )
        )

    def leerUsuarios(self):
        tabla(self.leer("select * from cliente"))

    def cargarUsuario(self):
        valores = cargar(
            ["id_cli", "nombre", "apellido", "telefono", "email"],
            [
                "el código de cliente (opcional)",
                "el nombre",
                "el apellido",
                "numero de telefono",
                "el E-Mail",
            ],
        )

        if valores:
            self.cargar("cliente", [*valores.values()])

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
                        "Por campo": self.leerVacasCampo,
                        "Por potrero": self.leerVacasPotrero,
                        "Por parcela": self.leerVacasParcela,
                        "Todos": self.leerVacasTodos,
                    },
                    "Cargar animal": self.cargarVaca,
                    "Cargar seguimiento": self.cargarSeguimiento,
                    "Modificar animal": self.modificarVaca,
                    "Eliminar animal": lambda: print("Eliminando un animal"),
                },
                "Campos, potreros y parcelas": {
                    "Campos": {
                        "Listar Campos": self.leerCampos,
                        "Cargar Campos": self.cargarCampo,
                        "Modificar Campos": lambda: print("Modificando Campos"),
                        "Eliminar Campos": lambda: print("Eliminando Campos"),
                    },
                    "Potreros": {
                        "Listar Potreros": self.leerPotreros,
                        "Cargar Potreros": self.cargarPotrero,
                        "Modificar Potreros": lambda: print("Modificando Potreros"),
                        "Eliminar Potreros": lambda: print("Eliminando Potreros"),
                    },
                    "Parcelas": {
                        "Listar Parcelas": self.leerParcelas,
                        "Cargar Parcelas": self.cargarParcela,
                        "Modificar Parcelas": lambda: print("Modificando Parcelas"),
                        "Eliminar Parcelas": lambda: print("Eliminando Parcelas"),
                    },
                },
                "Usuarios": {
                    "Listado de usuarios": self.leerUsuarios,
                    "Carga de usuarios": self.cargarUsuario,
                    "Modificación de usuarios": lambda: print(
                        "Modificación de usuarios"
                    ),
                    "Baja de usuarios": lambda: print("Baja de usuarios"),
                },
            }
        }

        self.menu = Menu(dicc)

        if seEjectua:
            self.menu.iniciar()

    def leer(self, query):
        return self.db.fetch(query)

    def cargar(self, tabla: str, datos: list) -> None:
        signos = ("?, " * (len(datos) - 1)) + "?"
        # Crea un string "(?, ?, ?)" con la cantidad de signos necesitada por la consulta

        self.db.insert("insert into {} values ({})".format(tabla, signos), datos)
        print("\nDatos cargados correctamente...")
        pass


# Observaciones mías:
# Cómo sé la cantidad de vacas por campo, potrero, y parcela?
# le agrego parcela a la vaca
# Qué valores se pueden modificar?
main = Main(False)
main.menu.iniciar()
