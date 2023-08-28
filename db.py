import sqlite3 as sql


class Db:
    def __init__(self) -> None:
        self.conn = sql.connect("base.sqlite3")

        self.conn.row_factory = sql.Row

        self.cur = self.conn.cursor()

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS cliente (
                    id_cli INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre VARCHAR2 NOT NULL,
                    apellido VARCHAR2 NOT NULL,
                    telefono VARCHAR2,
                    email VARCHAR2 NOT NULL
            )"""
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS animal (
                id_anim INTEGER PRIMARY KEY AUTOINCREMENT,
                id_padre INTEGER,
                id_madre INTEGER NOT NULL,
                fec_nac DATE NOT NULL,
                peso_nac FLOAT NOT NULL,
                sexo NUMBER(1) NOT NULL,
                cat INTEGER NOT NULL,
                sub_cat INTEGER NOT NULL,
                parc INTEGER NOT NULL,
                FOREIGN KEY (id_padre) REFERENCES animal (id_anim),
                FOREIGN KEY (id_madre) REFERENCES animal (id_anim),
                FOREIGN KEY (parc) REFERENCES parcela (id_parc)
            )
            """
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS campo (
                id_camp INTEGER PRIMARY KEY AUTOINCREMENT,
                fec_alta DATE NOT NULL,
                tipo_campo INTEGER NOT NULL,
                ancho FLOAT NOT NULL CHECK(ancho > 0),
                largo FLOAT NOT NULL CHECK(largo > 0),
                nombre VARCHAR2 NOT NULL,
                propietario VARCHAR2 NOT NULL,
                telefono VARCHAR2 NOT NULL,
                email VARCHAR2 NOT NULL

            )"""
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS potrero (
                id_pot INTEGER PRIMARY KEY AUTOINCREMENT,
                id_camp_pot INTEGER NOT NULL,
                ancho FLOAT NOT NULL CHECK(ancho > 0),
                largo FLOAT NOT NULL CHECK(largo > 0),
                car_animal FLOAT NOT NULL,
                vol_pasto_n FLOAT NOT NULL,
                vol_pasto_l FLOAT NOT NULL,
                FOREIGN KEY (id_camp_pot) REFERENCES campo (id_camp)
            )"""
        )
        # PASTO NATURAL E IMPLANTADO n y l

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS parcela (
                id_parc INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pot_parc INTEGER NOT NULL,
                observaciones TEXT NULL,
                ancho FLOAT NOT NULL CHECK(ancho > 0),
                largo FLOAT NOT NULL CHECK(largo > 0),
                FOREIGN KEY (id_pot_parc) REFERENCES potrero (id_pot)

            )"""
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS seguimiento (
                id_segui INTEGER PRIMARY KEY AUTOINCREMENT,
                id_anim_seg INTEGER NOT NULL,
                fec_seg DATE NOT NULL,
                estado_desc TEXT NOT NULL,
                fec_estimada DATE NOT NULL,
                FOREIGN KEY (id_anim_seg) REFERENCES animal (id_anim)
            )"""
        )

    def fetch(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data

    def ejecutar(self, query: str, datos=None):
        if datos:
            # print("el query es", query)
            self.cur.execute(query, list(datos))
        else:
            self.cur.execute(query)
        self.conn.commit()
        # Se podría pedir confirmación antes del commit pero no me dá el tiempo ahora
