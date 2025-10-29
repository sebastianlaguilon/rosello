\
import os
import mysql.connector
from mysql.connector import pooling

class _ConnectionCtx:
    """
    Provee una interfaz mínima compatible con:
        cur = mysql.connection.cursor()
        cur.execute(...)
        rows = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    Cada llamada a `mysql.connection` crea un contexto nuevo con su propia conexión del pool.
    """
    def __init__(self, pool, dict_default=False):
        self._pool = pool
        self._conn = None
        self._cur = None
        self._dict_default = dict_default

    def cursor(self, dictionary=None):
        if self._conn is None:
            self._conn = self._pool.get_connection()
        # Si no especifican, usamos el default (tuplas)
        use_dict = self._dict_default if dictionary is None else dictionary
        self._cur = self._conn.cursor(dictionary=use_dict)
        return self._cur

    def commit(self):
        if self._conn:
            self._conn.commit()

    def close(self):
        # cerrar cursor y conexión (libera el pool)
        try:
            if self._cur:
                self._cur.close()
        finally:
            if self._conn:
                self._conn.close()
            self._cur = None
            self._conn = None

class MySQL:
    def __init__(self):
        self.pool = None
        self._dict_default = False

    @property
    def connection(self):
        if not self.pool:
            raise RuntimeError("MySQL pool no inicializado. Llamá a init_app(app) primero.")
        return _ConnectionCtx(self.pool, self._dict_default)

mysql = MySQL()

def init_app(app):
    """
    Lee config desde app.config o variables de entorno.
    Crea un pool de conexiones mysql-connector.
    """
    host = app.config.get("MYSQL_HOST", os.getenv("MYSQL_HOST", "localhost"))
    port = int(app.config.get("MYSQL_PORT", os.getenv("MYSQL_PORT", "3306")))
    user = app.config.get("MYSQL_USER", os.getenv("MYSQL_USER", "root"))
    password = app.config.get("MYSQL_PASSWORD", os.getenv("MYSQL_PASSWORD", ""))
    database = app.config.get("MYSQL_DB", os.getenv("MYSQL_DB", "fumigadora_rosello"))
    charset = app.config.get("MYSQL_CHARSET", os.getenv("MYSQL_CHARSET", "utf8mb4"))
    cursorclass = app.config.get("MYSQL_CURSORCLASS", os.getenv("MYSQL_CURSORCLASS", ""))
    dict_default = True if str(cursorclass).lower() == "dictcursor" else False

    mysql._dict_default = dict_default

    mysql.pool = pooling.MySQLConnectionPool(
        pool_name="fr_pool",
        pool_size=int(os.getenv("MYSQL_POOL_SIZE", "5")),
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset=charset,
        use_pure=True,
        autocommit=False,
        collation="utf8mb4_unicode_ci",
    )
