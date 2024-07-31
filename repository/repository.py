import logging
from psycopg2 import DatabaseError
from domain.product import Product
from repository.databaseConnection import DatabaseConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Repository:
    def __init__(self):
        self.repository = DatabaseConnection()

    def create_product(self, product: Product):
        try:
            query = """INSERT INTO products (name, description, price, stock) 
                       VALUES (%s, %s, %s, %s) RETURNING id, name, description, price, stock"""
            params = (product.name, product.description, product.price, product.stock)
            result = self.repository.fetch_one(query, params)
            return result
        except DatabaseError as e:
            logger.error(f"Database error occurred during product creation: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during product creation: {e}")
            return None

    def get_product_by_id(self, id: str):
        try:
            query = "SELECT id, name, description, price, stock FROM products WHERE id = %s"
            params = (id,)
            result = self.repository.fetch_one(query, params)
            logger.debug(f"Fetched product: {result}")
            return result
        except DatabaseError as e:
            logger.error(f"Database error occurred while fetching product by id: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching product by id: {e}")
            return None

    def get_products(self):
        try:
            query = "SELECT id, name, description, price, stock FROM products"
            result = self.repository.fetch_all(query)
            return result
        except DatabaseError as e:
            logger.error(f"Database error occurred while fetching products: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching products: {e}")
            return None

    def delete_product(self, id: str):
        try:
            query = "DELETE FROM products WHERE id = %s RETURNING id"
            params = (id,)
            result = self.repository.fetch_one(query, params)
            logger.debug(f"Result from delete query: {result}")
            return result is not None
        except DatabaseError as e:
            logger.error(f"Database error occurred during product deletion: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during product deletion: {e}")
            return False

    def update_product(self, id: str, updated_product: Product):
        try:
            query = """
               UPDATE products SET
                   name = COALESCE(%s, name),
                   description = COALESCE(%s, description),
                   price = COALESCE(%s, price),
                   stock = COALESCE(%s, stock)
               WHERE id = %s
               RETURNING id, name, description, price, stock
            """
            params = (
                updated_product.name, updated_product.description, updated_product.price, updated_product.stock, id)
            result = self.repository.fetch_one(query, params)
            if not result:
                raise ValueError(f"Product (with id: {id}) not found.")
            return result
        except ValueError as e:
            logger.error(f"Value error occurred during product update: {e}")
            raise
        except DatabaseError as e:
            logger.error(f"Database error occurred during product update: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during product update: {e}")
            return None

    def update_stock(self, id: str, stock: int):
        try:
            query = "UPDATE products SET stock = stock + %s WHERE id = %s RETURNING id, name, description, price, stock"
            params = (stock, id)
            result = self.repository.fetch_one(query, params)
            return result
        except DatabaseError as e:
            logger.error(f"Database error occurred during stock update: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during stock update: {e}")
            return None

    def calculation_statistics(self):
        try:
            query = """
            SELECT COUNT(*) AS product_sum,
                   MAX(price) AS max_price,
                   MIN(price) AS min_price,
                   AVG(price) AS average_price,
                   SUM(stock) AS total_stock,
                   AVG(stock) AS average_stock
            FROM products
            """
            result = self.repository.fetch_all(query)
            statistic = result[0] if result else None
            return statistic
        except Exception as ex:
            logger.error(f"An error arose during product statistics calculation: {ex}")
            return None
