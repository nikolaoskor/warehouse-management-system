from sqlite3 import DatabaseError

from repository.repository import Repository, logger
from services.mapper import map_products, map_product_statistics
from domain.product import Product


class ProductServices:
    def __init__(self):
        self.repo = Repository()

    def create_product(self, product: Product):
        new_product = self.repo.create_product(product)
        return map_products([new_product]) if new_product else None

    def get_products(self):
        raw_data = self.repo.get_products()
        return map_products(raw_data) if raw_data else None

    def update_product(self, id: str, updated_product: Product):
        upd_product = self.repo.update_product(id, updated_product)
        return map_products([upd_product]) if upd_product else None

    def delete_product(self, id: str):
        return self.repo.delete_product(id)

    def get_product_by_id(self, id: str):
        raw_data = self.repo.get_product_by_id(id)
        logger.debug(f"Raw data from repository: {raw_data}")
        return map_products([raw_data]) if raw_data else None

    def manage_stock(self, id: str, operation: str, stock: int):
        try:
            query = "SELECT stock FROM products WHERE id = %s"
            params = (id,)
            current_stock_result = self.repo.repository.fetch_one(query, params)

            if not current_stock_result:
                raise ValueError("Product not found or unable to fetch current stock.")

            current_stock = current_stock_result[0]

            if operation == "plus":
                new_stock = current_stock + stock
            elif operation == "minus":
                new_stock = current_stock - stock
            else:
                raise ValueError("Invalid operation. Must be 'plus' or 'minus'")

            if new_stock < 0:
                raise ValueError("Stock cannot be negative.")

            result = self.repo.update_stock(id, stock if operation == "plus" else -stock)
            return map_products([result]) if result else None

        except ValueError as e:
            logger.error(f"Value error occurred during stock management: {e}")
            raise
        except DatabaseError as e:
            logger.error(f"Database error occurred during stock management: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during stock management: {e}")
            raise

    def get_product_statistic(self):
        try:
            statistic = self.repo.calculation_statistics()
            return map_product_statistics(statistic)
        except Exception as ex:
            print(f"An error arose during retrieving statistics: {ex}")
            return False
