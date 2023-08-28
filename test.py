def validar_fecha(fecha):
    if len(fecha) != 10:
        return False

    partes = fecha.split("-" if "-" in fecha else "/")
    if len(partes) != 3:
        return False

    year, month, day = partes

    if not year.isdigit() or not month.isdigit() or not day.isdigit():
        return False

    year = int(year)
    month = int(month)
    day = int(day)

    if 1900 <= year <= 9999 and 1 <= month <= 12 and 1 <= day <= 31:
        return True

    return False


# Ejemplos de fechas
fechas = ["2023-08-28", "2023/08/28", "23-08-28", "2023-08-32", "2023-13-28"]

for fecha in fechas:
    if validar_fecha(fecha):
        print(f"{fecha} es una fecha válida.")
    else:
        print(f"{fecha} no es una fecha válida.")
