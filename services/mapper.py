from domain.product import Product


def map_products(data: list):
    products = []
    for row in data:
        product = Product(
            name=row[1],
            description=row[2],
            price=row[3],
            stock=row[4]
        )
        products.append(product)
    return products


def map_product_statistics(statistic):
    if statistic:
        return {
            "product sum": statistic[0],
            "max price": statistic[1],
            "min price": statistic[2],
            "average price:": statistic[3],
            "total stock": statistic[4],
            "average stock": statistic[5]
        }
    else:
        return None
