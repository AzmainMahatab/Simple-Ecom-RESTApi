from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


products = []


@app.get("/products")
def get_products(category: str = None):
    if category:
        return [product for product in products if product['category'] == category]
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
def create_product(product: Product):
    products.append(product.dict())
    return product


@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index] = updated_product.dict()
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            del products[index]
            return {"detail": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
