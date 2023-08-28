from db import Db
from menu import Menu
import datetime

kilosPorMes = 25

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

idsIngreso = {"parc": ["parcela", "id_parc"]}
# campo en hijo: [tabla, campo en padre]

# Que valores pueden ser ingresados como nulos,
# Ya sea por que se autogeneran, como la foreign key,
# o por que no son estrictamente requeridos
# Se usa en ingresar()

fechas = ["fec_nac", "fec_alta", "fec_estimada", "fec_seg"]
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
    "id_anim": "Código animal",
    "id_padre": "Código padre",
    "id_madre": "Código madre",
    "fec_nac": "Nacimiento",
    "peso_nac": "Peso nacimiento",
    "sexo": "Sexo",
    "cat": "Categoría",
    "sub_cat": "Subcategoría",
    "parc": "Parcela",
    "id_camp": "Código campo",
    "fec_alta": "Fecha de alta",
    "tipo_campo": "Tipo",
    "nombre": "Nombre",
    "propietario": "Propietario",
    "telefono": "Teléfono",
    "email": "E-Mail",
    "hectareas": "Hectáreas",
    "id_pot": "Código potrero",
    "id_camp_pot": "Código campo",
    "ancho": "Ancho",
    "largo": "Largo",
    "car_animal": "Carga animal",
    "vol_pasto_n": "Volumen pasto N",
    "vol_pasto_l": "Volumen pasto L",
    "id_parc": "Código parcela",
    "id_pot_parc": "Código potrero",
    "observaciones": "Observaciones",
    "id_cli": "Código ciente",
    "apellido": "Apellido",
    "fec_seg": "Fecha del seguimiento",
    "id_segui": "Código de seguimiento",
    "id_anim_seg": "Animal del seguimiento",
    "fec_estimada": "Fecha estimada de parición",
    "estado_desc": "Descripción del estado",
    "potreros": "N° de potreros",
    "parcelas": "N° de parcelas",
    "animales": "N° de animales",
}


def confirmar():
    while True:
        print("Confirma la operación?")
        v = input("Si, No: ").lower().strip()

        if v in ("si", "s", "1"):
            return True
        elif v in ("no", "n", 0):
            return False

        print("No valido, reintente...")


def ingresar(
    paraQue,
    variable,
    coso,
    datoViejo=None,
):
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

    if variable in idsIngreso.keys():
        print("Los códigos disponibles son: ")
        txt = ""
        posibles = []
        print(
            "a coso es ",
            "select {} from {}".format(
                idsIngreso[variable][1],
                idsIngreso[variable][0],
            ),
        )
        for i in coso.leer(
            "select {} from {}".format(
                idsIngreso[variable][1],
                idsIngreso[variable][0],
            )
        ):
            posibles.append(i[idsIngreso[variable][1]])
            txt += str(i[idsIngreso[variable][1]]) + ","

        print(txt[:-1])

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
                valor = valor.strip().lower()
                ano = valor[:4]
                mes = valor[5:]

                if mes.isdigit() and ano.isdigit():
                    ano = int(ano)
                    mes = int(mes)

                    if 1900 < ano < int(datetime.datetime.now().year):
                        if 0 < mes < 13:
                            return valor

                print("Ingrese una fecha válida")
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

            elif variable in idsIngreso.keys():
                if valor.isnumeric():
                    valor = int(valor)
                    if valor in posibles:
                        return valor
                    print("No está en los disponibles")
                else:
                    print("Ingrese un número")
            else:
                if valor.isnumeric():
                    return int(valor)

                else:
                    print("Ingrese un entero positivo")


# Funciones de apoyo
def cargar(datos, textos, self, datos_viejos=None):
    # len datos debe corresponder con len textos
    # los datos a cargar son como va en el registro
    # Textos es visual

    indice = 0
    diccionario = {}
    for llave, texto in zip(datos, textos):
        # Le paso los datos viejos si estamos modificando, si no, no
        c = ingresar(texto, llave, self, datos_viejos[indice] if datos_viejos else None)
        if c == "CANCELAMOS":
            return
        diccionario[llave] = c
        indice += 1

    # Confirmación
    print("\nDatos cargados: ")
    # tabla() si o sí me pide una lista de diccionarios así que tiene que ir así

    for key, value in diccionario.items():
        if value:
            if key in rangos:
                print(f"{diccTitulos[key]}: {rangos[key][value-1]}")

            else:
                print(f"{diccTitulos[key]}: {value}")

        else:
            print(f"{diccTitulos[key]}: -")
    print("")

    if confirmar():
        return diccionario
    else:
        return


def tabla(datos):
    if not datos:
        print("No hay registros para mostrar...")
        return
    anchos = []
    header = ""

    # TODO: ver que hacemos con el ancho
    # podría ver de aprender a manejar curses pero ya fue

    for dato in datos[0].keys():
        dt = f" {diccTitulos[dato]} "

        anchos.append(len(dt))

        header += dt

    print(header)

    for linea in datos:
        lineaTexto = ""
        keys = [*linea.keys()]

        for i, dato in enumerate(linea):
            # Si la key está dentro de los rangos, en vez del dato presento el valor asociado
            # Se puede expandir para otros tipos de dato mas o menos fácil
            # print(f"dato {dato} i {i} keys[i] {keys[i]}")
            if keys[i] in rangos:
                lineaTexto += str(rangos[keys[i]][int(dato) - 1]).center(anchos[i])
            elif dato == None:
                lineaTexto += "-".center(anchos[i])
            else:
                lineaTexto += str(dato).center(anchos[i])

        print(lineaTexto)
    print("")
    print(f"Total: {len(datos)}")

    # TODO: Acá hago el cálculo de la carga de animales
    if "ancho" in datos[0].keys():
        sup = datos[0]["ancho"] * datos[0]["largo"]
        print(f"La superficie es {sup}")
        ahora = datetime.now()

        totalPeso = 0

        for i in datos:
            fecha = datetime(i["fec_nac"])
            meses = ahora.year * 12 + ahora.month - (fecha.year * 12 + fecha.month)

            totalPeso = meses * kilosPorMes

        print(f"Y en total las vacas comen {totalPeso * 0.03}kg por día")


class Main:
    def validarEnTabla(self, tabla, idN, msj="Ingrese el código para buscar"):
        print(msj)

        # Esto lo agregué después así que no es tan eficiente
        # Hace las búsquedas dos veces y no se
        disp = self.leer("select {} from {}".format(idN, tabla))

        print("Códigos disponibles:")
        print(*[str(d[idN]) for d in disp], sep=", ")
        # Magia kjasd para hacer menos código

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
                        print("No se encuentra ese código")
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
            self,
        )

        if valores:
            self.cargar(
                "animal",
                [*valores.values()],
            )
        else:
            print("Se canceló la operación")

    def modificarVaca(self):
        # TODO: ver que hago con esto, que valores se puede modificar y que nop
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
            self,
            self.leer(
                "select id_padre, id_madre, fec_nac, peso_nac, sexo, cat, sub_cat, parc from animal where id_anim = {}".format(
                    idObj
                )
            )[0],
        )
        if datos:
            self.modificar("animal", datos, "id_anim", idObj)

    def modificarSeguimiento(self):
        idObj = self.validarEnTabla("seguimiento", "id_segui")

        datos = cargar(
            ["id_anim_seg", "estado_desc", "fec_estimada"],
            [
                "el código del nuevo animal",
                "la nueva descripción",
                "la nueva fecha estimada de nacimiento",
            ],
            self,
            self.leer(
                "select id_anim_seg, fec_seg, estado_desc, fec_estimada from seguimiento where id_segui = {}".format(
                    idObj
                )
            )[0],
        )
        if datos:
            self.modificar("seguimiento", datos, "id_seg", idObj)

    def modificarCampo(self):
        idObj = self.validarEnTabla("campo", "id_camp")

        datos = cargar(
            [
                "fec_alta",
                "tipo_campo",
                "ancho",
                "largo",
                "nombre",
                "propietario",
                "telefono",
                "email",
            ],
            [
                "la nueva fecha de alta",
                "el nuevo tipo de campo",
                "el nuevo ancho",
                "el nuevo largo",
                "el nuevo nombre",
                "el nuevo propietario",
                "el nuevo teléfono",
                "el nuevo E-Mail",
            ],
            self,
            self.leer(
                "select fec_alta, tipo_campo, ancho, largo, nombre, propietario, telefono, email from campo where id_camp = {}".format(
                    idObj
                )
            )[0],
        )
        if datos:
            self.modificar("campo", datos, "id_camp", idObj)

    def modificarPotrero(self):
        idObj = self.validarEnTabla("potrero", "id_pot")

        datos = cargar(
            [
                "id_camp_pot",
                "ancho",
                "largo",
                "car_animal",
                "vol_pasto_n",
                "vol_pasto_l",
            ],
            [
                "el nuevo campo",
                "el nuevo ancho",
                "el nuevo largo",
                "la nueva carga animal",
                "el nuevo v. de pasto natural",
                "el nuevo v. de pasto implantado",
            ],
            self,
            self.leer(
                "select id_camp_pot, ancho, largo, car_animal, vol_pasto_n, vol_pasto_l from potrero where id_pot = {}".format(
                    idObj
                )
            )[0],
        )
        if datos:
            self.modificar("potrero", datos, "id_pot", idObj)

    def modificarParcela(self):
        idObj = self.validarEnTabla("parcela", "id_parc")

        datos = cargar(
            ["id_pot_parc", "observaciones", "ancho", "largo"],
            [
                "el nuevo potrero",
                "las nuevas observaciones",
                "el nuevo ancho",
                "el nuevo largo",
            ],
            self,
            self.leer(
                "select id_pot_parc, observaciones, ancho, largo from parcela where id_parc = {}".format(
                    idObj
                )
            )[0],
        )

        if datos:
            self.modificar("parcela", datos, "id_parc", idObj)

    def modificarUsuario(self):
        idObj = self.validarEnTabla("cliente", "id_cli")

        datos = cargar(
            ["nombre", "apellido", "telefono", "email"],
            [
                "el nuevo nombre",
                "el nuevo apellido",
                "el nuevo teléfono",
                "el nuevo E-Mail",
            ],
            self,
            self.leer(
                "select nombre, apellido, telefono, email from cliente where id_cli = {}".format(
                    idObj
                )
            )[0],
        )
        if datos:
            self.modificar("cliente", datos, "id_cli", idObj)

    def cargarCampo(self):
        valores = cargar(
            [
                "id_camp",
                "fec_alta",
                "tipo_campo",
                "ancho",
                "largo",
                "nombre",
                "propietario",
                "telefono",
                "email",
            ],
            [
                "el código del campo (Opcional)",
                "la fecha de inicio de producción",
                "el tipo de campo",
                "el ancho del campo",
                "el largo del campo",
                "el nombre del campo",
                "el propietario",
                "el telefono asociado",
                "el e-mail asociado",
            ],
            self,
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
            self,
        )

        if valores:
            self.cargar("potrero", [*valores.values()])

    def cargarParcela(self):
        valores = cargar(
            [
                "id_parc",
                "id_pot_parc",
                "observaciones",
                "ancho",
                "largo",
            ],
            [
                "el código de la parcela (opcional)",
                "el potrero donde está",
                "otras observaciones (opcional)",
                "el ancho de la parcela",
                "el largo de la parcela",
            ],
            self,
        )

        if valores:
            self.cargar("parcela", [*valores.values()])

    def cargarSeguimiento(self):
        valores = cargar(
            ["id_segui", "id_anim_seg", "fec_seg", "estado_desc", "fec_estimada"],
            [
                "el código de seguimiento (opcional)",
                "el código del animal",
                "la fecha del seguimiento",
                "la descripción",
                "la fecha estimada de nacimiento",
            ],
            self,
        )

        if valores:
            self.cargar("seguimiento", [*valores.values()])

    def leerVacasCampo(self):
        campo = self.validarEnTabla("campo", "id_camp")
        if campo:
            tabla(
                self.leer(
                    """select animal.*, id_pot, campo.ancho as ancho, campo.largo as largo
                    from animal
                    join parcela on id_parc = parc
                    join potrero on id_pot = id_pot_parc
                    join campo on id_camp = id_camp_pot
                    where id_camp = {}""".format(
                        campo
                    )
                )
            )

    def leerVacasPotrero(self):
        pot = self.validarEnTabla("potrero", "id_pot")
        if pot:
            tabla(
                self.leer(
                    """select animal.*, id_pot, potrero.ancho as ancho, potrero.largo as largo from animal
                    join parcela on id_parc = parc
                    join potrero on id_pot = id_pot_parc
                    where id_pot = {}""".format(
                        pot
                    )
                )
            )

    def leerVacasParcela(self):
        parcela = self.validarEnTabla("parcela", "id_parc")
        if parcela:
            tabla(
                self.leer(
                    """select animal.*, id_pot, parcela.ancho, parcela.largo from animal
                    join parcela on id_parc = parc
                    join potrero on id_pot = id_pot_parc
                    where id_parc = {}""".format(
                        parcela
                    )
                )
            )

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
            self,
        )

        if valores:
            self.cargar("cliente", [*valores.values()])

    def leerSeguimientos(self):
        idObj = self.validarEnTabla("animal", "id_anim")

        valores = self.leer(
            "select id_segui, fec_seg, estado_desc, fec_estimada from seguimiento where id_anim_seg = {}".format(
                idObj
            )
        )
        if not valores:
            print(f"No hay seguimientos registrados para el animal {idObj}")
            return
        print(f"\nAnimal: {idObj}")

        for linea in valores:
            print(f"Fecha: {linea['fec_seg']}")
            if linea["estado_desc"]:
                print(f"Descripción: {linea['estado_desc']}")
            else:
                print("No se registró descripción")

            if linea["fec_estimada"]:
                print(f"Fecha estimada de parición: {linea['fec_estimada']}")
            else:
                print("No hay fecha de parición estimada")

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
                        "Todos": lambda: self.funcionLeer(
                            "select animal.*, potrero.id_pot as id_pot from animal join parcela on id_parc = parc join potrero on id_pot = id_pot_parc   "
                        ),
                    },
                    "Cargar animal": self.cargarVaca,
                    "Modificar animal": self.modificarVaca,
                    "Eliminar animal": lambda: self.eliminar("animal", "id_anim"),
                },
                "Seguimientos": {
                    "Listar seguimientos": self.leerSeguimientos,
                    "Cargar seguimiento": self.cargarSeguimiento,
                    "Modificar seguimiento": self.modificarSeguimiento,
                    "Eliminar seguimiento": lambda: self.eliminar(
                        "seguimiento", "id_seg"
                    ),
                },
                "Campos, potreros y parcelas": {
                    "Campos": {
                        "Listar Campos": lambda: self.funcionLeer(
                            """select campo.*, count(pot.id_pot) as potreros, count(par.id_parc) as parcelas, count(a.id_anim) as animales
                            from campo
                            left join potrero as pot
                            on id_camp_pot = id_camp
                            left join parcela as par
                            on id_pot_parc = id_pot
                            left join animal as a
                            on a.parc = id_parc
                            group by id_camp"""
                        ),
                        "Cargar Campos": self.cargarCampo,
                        "Modificar Campos": self.modificarCampo,
                        "Eliminar Campos": lambda: self.eliminar("campo", "id_camp"),
                    },
                    "Potreros": {
                        "Listar Potreros": lambda: self.funcionLeer(
                            "select potrero.*, count(id_parc) as parcelas, count(id_anim) as animales from potrero left join parcela on id_pot_parc = id_pot lef join animal on parc = id_parc group by id_pot"
                        ),
                        "Cargar Potreros": self.cargarPotrero,
                        "Modificar Potreros": self.modificarPotrero,
                        "Eliminar Potreros": lambda: self.eliminar("potrero", "id_pot"),
                    },
                    "Parcelas": {
                        "Listar Parcelas": lambda: self.funcionLeer(
                            "select parcela.*, id_camp_pot, count(id_anim) as animales from parcela left join potrero on id_pot = id_pot_parc left join animal on parc = id_parc group by id_parc"
                        ),
                        "Cargar Parcelas": self.cargarParcela,
                        "Modificar Parcelas": self.modificarParcela,
                        "Eliminar Parcelas": lambda: self.eliminar(
                            "parcela", "id_parc"
                        ),
                    },
                },
                "Usuarios": {
                    "Listado de usuarios": lambda: self.funcionLeer(
                        "select * from cliente"
                    ),
                    "Carga de usuarios": self.cargarUsuario,
                    "Modificación de usuarios": self.modificarUsuario,
                    "Baja de usuarios": lambda: self.eliminar("cliente", "id_cli"),
                },
            }
        }

        self.menu = Menu(dicc)

        if seEjectua:
            self.menu.iniciar()

    def leer(self, query):
        return self.db.fetch(query)

    def funcionLeer(self, query):
        tabla(self.leer(query))

    def cargar(self, tabla: str, datos: list) -> None:
        signos = ("?, " * (len(datos) - 1)) + "?"
        # Crea un string "(?, ?, ?)" con la cantidad de signos necesitada por la consulta

        self.db.ejecutar("insert into {} values ({})".format(tabla, signos), datos)
        print("\nDatos cargados correctamente...")

    def modificar(self, tabla: str, datos, idN: str, id: int):
        query = "UPDATE {} SET".format(tabla)

        for key in datos.keys():
            query += f" {key} = ?,"

        query = query[:-1]  # Le saco la última coma que no va

        query += f" WHERE {idN} = {id}"

        self.db.ejecutar(query, datos.values())

    def eliminar(self, tabla: str, idN: str) -> None:
        id = self.validarEnTabla(tabla, idN)
        if id:
            if confirmar():
                # Validar que no elimine nada que lo deje huérfano
                self.db.ejecutar("DELETE FROM {} where {} = {}".format(tabla, idN, id))
            else:
                print("No se eliminaron datos")


# Validar existencias de parcelas, campos y port
# Validar ingreso de información repetida
# Validar ingreso de fechas correctas

# Observaciones mías:
# Cómo sé la cantidad de vacas por campo, potrero, y parcela?
# A cada vaca le doy una parcela
# le agrego parcela a la vaca

# Qué valores se pueden modificar?
# Yo dejo que se modifique todo por ahora

# Que es pasto N y pasto I? para que se usa?
# Para qué cargo los usuarios? se van a usar en algún momento?

# La carga animal es el máximo de animales? o los que hay ahora? yo lo tomaría como máximo

# Cuanta materia seca se produce por día? mes?  cuanto pesa una vaca?

# __________________________________________
# De lo que chusmié en otros trabajos
# Cambiar todos los animales un potrero a otro, por ahora se hace animal por animal eso

# categorías vientre, vaquita 1 año, 2 años, ternero y toro
# Subcategorías de vientre: 1ra parición, 2da parición, vaca, y2 descarte

# Carga y peso
# Cada animal come 3% del peso
# Cómo hago eso? 1m cuadrado es 1kg de materia seca? cuanto pesa cada vaca? solo tengo el peso inicial
# Hice un modelito burdo como para tener algo, le sumo 25kg por més de vida a la vaca

main = Main(False)
main.menu.iniciar()
