import json
from typing import List

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict):
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**item) for item in data['contents']],
            cost=data['cost']
        )

def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        contents = json.loads(cart_detail['contents'])
        items.extend(contents)

    # Batch product retrieval to reduce requests per second
    if items:
        products_info = products.get_products_by_ids(items)  # Assume this function retrieves products in bulk
        return [Product(**product) for product in products_info]
    return []

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)
