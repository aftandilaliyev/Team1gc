from sqlalchemy.orm import Session

from backend.src.shared.schemas.payment import WebhookRequest


class OrderService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_the_cart(self, user_id):
        pass

    def add_to_the_cart(self, user_id, product_id, quantity):
        pass

    def remove_from_the_cart(self, user_id, product_id):
        pass

    def checkout(self, user_id):
        pass

    def handle_webhook(self, payload: WebhookRequest):
        # TODO: creates order
        pass

    def get_order_status(self, user_id, order_id):
        pass
