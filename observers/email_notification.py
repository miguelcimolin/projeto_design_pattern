from .base_observer import Observer

class EmailNotification(Observer):
    def update(self, order):
        state_name = order.state.__class__.__name__ if order.state else "Nenhum (finalizado)"
        print(f"[Email] Notificando via e-mail: Pedido {order.order_id} mudou para {state_name}.")
