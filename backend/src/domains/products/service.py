from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session


class ProductService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def query_products(
        self,
        page,
        elements,
        price_min,
        price_max,
        category,
        sort,
        search
    ):
        pass

    def get_product_by_id(self, product_id):
        pass

    def create_product(self, create_product_schema):
        pass

    def update_product(self, update_product_schema):
        pass

    def delete_product(self, product_id):
        pass
