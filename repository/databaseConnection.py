import psycopg2
from psycopg2 import OperationalError
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self):
        self.dbname = "postgres"
        self.user = "postgres"
        self.password = "pass123"
        self.host = "localhost"
        self.port = "5432"

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            yield conn
        except OperationalError as ex:
            logger.error(f"An error occurred while connecting to the database: {ex}")
            raise
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_cursor(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception as ex:
                conn.rollback()
                logger.error(f"An error occurred while executing the query: {ex}")
                raise
            finally:
                cursor.close()

    def execute_query(self, query: str, params: tuple = ()):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor

    def fetch_one(self, query: str, params: tuple = ()):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
