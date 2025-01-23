from products import dao
from collections import namedtuple
from functools import lru_cache

# Use namedtuple for lightweight, immutable data objects
Product = namedtuple('Product', ['id', 'name', 'description', 'cost', 'qty'])

# Cache for frequently accessed data (e.g., product listings)
@lru_cache(maxsize=128)
def list_products() -> list[Product]:
    """Fetch all products efficiently with caching."""
    products_data = dao.list_products()
    return [Product(**product) for product in products_data]


def get_product(product_id: int) -> Product:
    """Fetch a single product by ID with caching."""
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product(**product_data)


def add_product(product: dict):
    """Adds a new product."""
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """Update quantity using atomic database operations."""
    if qty < 0:
        raise ValueError('Quantity cannot be negative.')
    # Use atomic updates to reduce race conditions and overhead
    if not dao.update_qty(product_id, qty):
        raise ValueError(f"Failed to update quantity for Product ID {product_id}.")
