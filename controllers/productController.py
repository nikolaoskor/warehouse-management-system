from fastapi import APIRouter, HTTPException
from repository.databaseConnection import logger
from services.productServices import ProductServices
from domain.product import Product, StockPayLoad

router = APIRouter()
service = ProductServices()


@router.post('/new')
async def create_product(product: Product):
    new_product = service.create_product(product)
    if new_product:
        return {"message": f"Product: {product.name} has been successfully created with price: {product.price}€ ",
                "product": new_product}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate the requested product.")


@router.get('/all')
async def get_products():
    products = service.get_products()
    if products:
        return products
    else:
        raise HTTPException(status_code=404, detail="Products not found")


@router.put('/update/{id}')
async def update_product(id: str, product: Product):
    try:
        updated_product = service.update_product(id, product)
        if updated_product:
            return {"message": f"Product (with id: {id}) has been successfully updated",
                    "product": updated_product}
        else:
            raise HTTPException(status_code=500, detail="Failed to update product")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update product")


@router.delete('/delete/{id}')
async def delete_product(id: str):
    logger.debug(f"Deleting product with ID: {id}")
    result = service.delete_product(id)
    logger.debug(f"Result from service delete_product: {result}")
    if result:
        return {"message": f"Product with ID: {id} has been successfully deleted."}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete product")


@router.get('/{id}')
async def get_product_by_id(id: str):
    logger.debug(f"Fetching product with ID: {id}")
    product = service.get_product_by_id(id)
    if product:
        logger.debug(f"Found product: {product}")
        return product
    else:
        logger.error(f"Product with ID {id} not found")
        raise HTTPException(status_code=404, detail=f"Product (with ID: {id}) not found")


@router.put('/manage/{id}')
async def manage_stock(id: str, payload: StockPayLoad):
    try:
        managed_product = service.manage_stock(id, payload.operation, payload.stock)

        if managed_product:
            if payload.operation == 'plus':
                message = "Product stock has been successfully increased."
            elif payload.operation == 'minus':
                message = "Product stock has been successfully decreased."
            else:
                raise ValueError("Invalid operation type. Use 'plus' or 'minus'.")

            return {"message": message, "product": managed_product}
        else:
            raise HTTPException(status_code=500,
                                detail=f"Failed to manage product stock with operation: {payload.operation}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Failed to manage product stock with operation: {payload.operation}")


@router.get('/products/statistics')
async def get_product_statistic():
    statistic = service.get_product_statistic()
    return {"statistics": statistic}
