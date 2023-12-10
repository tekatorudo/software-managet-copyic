import pyodbc
import config as cf


class Conn:
    def conn(self) -> pyodbc.Connection:
        return pyodbc.connect(cf.CONN_STRING)

    @property
    def cursor(self) -> pyodbc.Cursor:
        return self.conn().cursor()
