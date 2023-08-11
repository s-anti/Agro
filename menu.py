class Menu:

    """Una clase para hacer menúes que sean
    adaptables en base a diccionarios"""

    def __init__(self, dicc: dict, linea: str = "______________________"):
        # linea es el separador que vamos a usar
        self.linea = linea

        # dicc es el diccionario principal de la clase
        self.dicc = dicc

    def validar(self, numeros: tuple):
        # Función de validación, va desde numeros[0] a numeros[-1]
        # pero excluye todos los del medio
        while True:
            v = input(f"Ingrese un valor ({numeros[0]} - {numeros[-1]}): ")

            if not v.isnumeric():
                print("Debe ingresar un número...\n")
                continue

            v = int(v)

            if not numeros[0] <= v <= numeros[1]:
                print(f"Debe ser entre {numeros[0]} - {numeros[-1]}...\n")
                continue
            return v

    def recursiva(self, diccionario, llave):
        while True:
            print(llave)  # Titulo principal
            print(self.linea)

            numero = 0
            for opcion in diccionario[llave]:
                numero += 1
                print(f"{numero}: {opcion}")

            print(self.linea)

            print("0: Salir")

            print("\n" * 1)

            # numero es la ultima opcion
            opcion = self.validar((0, numero))
            print("\n" * 1)

            if opcion == 0:
                break

            # key de la opcion seleccionada, ej: "Submenu propietarios"
            nombre_opcion = list(diccionario[llave].keys())[opcion - 1]

            # Valor de esta opcion seleccionada
            item_menu = diccionario[llave][nombre_opcion]

            # Si la opcion es otro diccionario
            if isinstance(item_menu, dict):
                self.recursiva(diccionario[llave], nombre_opcion)

            # Si no lo es, llamamos la función que contiene
            elif callable(item_menu):
                item_menu()
                print("\n")

            # Si todo salió bien, repetimos el bucle

    def iniciar(self):
        self.recursiva(self.dicc, [*self.dicc.keys()][0])


if __name__ == "__main__":
    # Solo se ejecuta si ejecutamos este código, no si lo importamos en otro lado
    # Para revisar bugs más rápido
    mi_menu = {
        "Menu principal": {
            "Menu Ingresar": {
                "Ingresar Proveedores": lambda: print("Ingresar Proveedores"),
                "Ingresar Productos": lambda: print("Ingresar Productos"),
            },
            "Menu Leer": {
                "Menu secreto misterioso": {
                    "Opcion 1": lambda: print("Opcion 1"),
                    "Opcion 2": lambda: print("Opcion 2"),
                },
                "Leer Proveedores": lambda: print("Leer Proveedores"),
                "Leer Productos": lambda: print("Leer Productos"),
            },
            "Menu Actualizar": {
                "Actualizar Proveedores": lambda: print("Actualizar Proveedores"),
                "Actualizar Productos": lambda: print("Actualizar Productos"),
            },
            "Menu Eliminar": {
                "Eliminar Proveedores": lambda: print("Eliminar Proveedores"),
                "Eliminar Productos": lambda: print("Eliminar Productos"),
            },
        }
    }
