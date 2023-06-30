import sqlite3 as sql


class Main:
    def __init__(self) -> None:
        self.conn = sql.connect("base.sqlite3")
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
                hembra BOOLEAN NOT NULL,
                cat INTEGER NOT NULL,
                sub_cat INTEGER NOT NULL,
                FOREIGN KEY (id_padre) REFERENCES animal (id),
                FOREIGN KEY (id_madre) REFERENCES animal (id)
            )
            """
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS campo (
                id_camp INTEGER PRIMARY KEY AUTOINCREMENT,
                fec_alta DATE NOT NULL,
                tipo_campo INTEGER NOT NULL,
                nombre VARCHAR2 NOT NULL,
                propietario VARCHAR2 NOT NULL,
                telefono VARCHAR2 NOT NULL,
                main VARCHAR2 NOT NULL,
                hectareas FLOAT NOT NULL
            )"""
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS potrero (
                id_pot INTEGER PRIMARY KEY AUTOINCREMENT,
                id_camp INTEGER NOT NULL,
                ancho FLOAT NOT NULL CHECK(ancho > 0),
                largo FLOAT NOT NULL CHECK(largo > 0),
                car_animal FLOAT NOT NULL,
                vol_pasto_n FLOAT NOT NULL,
                vol_pasto_l FLOAT NOT NULL,
                FOREIGN KEY (id_camp) REFERENCES campo (id)
            )"""
        )
        # PASTO NATURAL E IMPLANTADO n y l

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS parcela (
                id_parc INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pot INTEGER NOT NULL,
                observaciones TEXT NULL,
                FOREIGN KEY (id_pot) REFERENCES potrero (id)

            )"""
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS seguimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_anim INTEGER NOT NULL,
                estado_desc TEXT NOT NULL,
                fec_estimada DATE NOT NULL,
                FOREIGN KEY (id_anim) REFERENCES animal (id)
            )"""
        )


a = Main()
