from .base_observer import Observer

class SMSNotification(Observer):
    def update(self, order):
        state_name = order.state.__class__.__name__ if order.state else "Nenhum (finalizado)"
        print(f"[SMS] Enviando SMS: Pedido {order.order_id} mudou para {state_name}.")
