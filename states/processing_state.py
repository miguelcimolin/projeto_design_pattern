import time
from .completed_state import CompletedState
from .base_state import OrderState

class ProcessingState(OrderState):
    def handle(self, order):
        print(f"[{order.order_id}] O pedido está sendo processado.")
        time.sleep(1)
        print(f"[{order.order_id}] Transição para: Pedido finalizado.")
        order.set_state(CompletedState())
