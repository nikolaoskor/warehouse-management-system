from fastapi import FastAPI
from controllers.productController import router as get_products

app = FastAPI()

app.include_router(get_products, prefix='/product')

# uvicorn main:app --port 8080 --reload
