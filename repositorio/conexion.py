"""Conexión a SQLite con la librería oficial sqlite3 (biblioteca estándar de Python).
La ruta de la base se lee desde la variable de entorno ECOTECH_DB_PATH (archivo .env)."""
import os
import sqlite3
from pathlib import Path

from dominio.excepciones import ErrorBaseDatos, ErrorConexionBD

RAIZ = Path(__file__).resolve().parent.parent
RUTA_SCHEMA = RAIZ / "datos" / "schema.sql"


def cargar_env(ruta=None):
    """Lee las líneas CLAVE=VALOR del archivo .env (si existe) hacia os.environ.
    Una variable ya definida en el sistema tiene prioridad sobre el archivo."""
    archivo = Path(ruta) if ruta else RAIZ / ".env"
    if not archivo.is_file():
        return
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        os.environ.setdefault(clave.strip(), valor.strip())


class ConexionBD:
    def __init__(self, ruta=None):
        cargar_env()
        ruta = ruta or os.environ.get("ECOTECH_DB_PATH", "ecotech.db")
        if str(ruta) == ":memory:":          # base temporal en memoria (la usa la demostración)
            self.__ruta = ":memory:"
        else:
            ruta = Path(ruta)
            self.__ruta = ruta if ruta.is_absolute() else RAIZ / ruta
        self.__conexion = None

    @property
    def ruta(self):
        return self.__ruta

    def conectar(self):
        try:
            self.__conexion = sqlite3.connect(self.__ruta)
            self.__conexion.execute("PRAGMA foreign_keys = ON")   # activa las llaves foráneas
        except sqlite3.Error as error:
            self.__conexion = None
            raise ErrorConexionBD(f"No fue posible conectar con la base de datos: {error}") from error
        return self.__conexion

    @property
    def conexion(self):
        if self.__conexion is None:
            self.conectar()
        return self.__conexion

    def inicializar_bd(self):
        try:
            self.conexion.executescript(RUTA_SCHEMA.read_text(encoding="utf-8"))
            self.conexion.execute("PRAGMA foreign_keys = ON")
        except (sqlite3.Error, OSError) as error:
            raise ErrorBaseDatos(f"No se pudo crear el esquema: {error}") from error

    def probar_conexion(self):
        try:
            return self.conexion.execute("SELECT sqlite_version()").fetchone()[0]
        except sqlite3.Error as error:
            raise ErrorConexionBD(f"La conexión no responde: {error}") from error

    def cerrar(self):
        if self.__conexion is not None:
            self.__conexion.close()
            self.__conexion = None


def inicializar_bd(ruta=None):
    """Crea las tablas (si no existen). Se puede invocar desde la terminal."""
    bd = ConexionBD(ruta)
    try:
        bd.inicializar_bd()
        print(f"Base de datos lista en: {bd.ruta}")
    finally:
        bd.cerrar()
