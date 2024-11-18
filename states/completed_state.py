from .base_state import OrderState

class CompletedState(OrderState):
    def handle(self, order):
        print(f"[{order.order_id}] Pedido finalizado e pronto para envio.")
        order.complete_order()  # Finaliza o pedido corretamente
