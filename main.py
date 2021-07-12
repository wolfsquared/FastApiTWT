from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {
    1: {}

}


@app.get("/")
def home():
    return {"Data": "Testing"}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The Id of the item you would like to view", gt=0, lt=3)):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item(name: Optional[str]):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not Found"}


@app.get("/about")
def about():
    return {"Data": "About"}


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists"}

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exist"}

    inventory[item_id].update(item)

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]
