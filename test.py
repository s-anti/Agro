import datetime

valor = "2002-10"

print(valor[:4], valor[5:])
valor = datetime.datetime(int(valor[:4]), int(valor[5:]), 0)
print(valor, " Es valor")
