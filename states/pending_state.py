import time
from .processing_state import ProcessingState
from .base_state import OrderState

class PendingState(OrderState):
    def handle(self, order):
        print(f"[{order.order_id}] O pedido está aguardando pagamento.")
        time.sleep(1)
        print(f"[{order.order_id}] Transição para: Processando pedido.")
        order.set_state(ProcessingState())
