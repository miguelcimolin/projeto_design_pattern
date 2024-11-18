import uuid
import sqlite3
from datetime import datetime
from models.order import Order
from states.pending_state import PendingState
from observers.email_notification import EmailNotification
from observers.sms_notification import SMSNotification
from functions import generate_client_data, get_next_sequencial, initialize_db
import time

initialize_db()

def criar():
    print("Sistema de Gestão de Pedidos\n")

    db_path = "bd/banco.db"

    order_id = str(uuid.uuid4())
    nome_cliente, cpf_cliente = generate_client_data()
    sequencial = get_next_sequencial(db_path)
    data_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO ordem (id, sequencial, nome_cliente, cpf_cliente, data_compra, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order_id, sequencial, nome_cliente, cpf_cliente, data_compra, "PendingState"))

    conn.commit()
    conn.close()

    print(f"Pedido criado com sucesso!")
    print(f"ID: {order_id}")
    print(f"Sequencial: {sequencial}")
    print(f"Cliente: {nome_cliente}")
    print(f"CPF: {cpf_cliente}")
    print(f"Data da compra: {data_compra}")

    order = Order(order_id)

    email_notifier = EmailNotification()
    sms_notifier = SMSNotification()
    order.add_observer(email_notifier)
    order.add_observer(sms_notifier)

    order.set_state(PendingState())

    while order.state is not None:
        order.start_processing()
        time.sleep(2)
        if order.state is None:
            print(f"\nO pedido {order.order_id} foi finalizado com sucesso!\n")
            break

def main():
    while True:
        print("\n---------------")
        print("Selecione uma opção:")
        print("1 - Criar novo Pedido")
        print("2 - Consultar Resultados")
        print("0 - Sair")
        print("---------------")

        resposta = input("Digite sua escolha: ").strip()

        if resposta == "1":
            criar()
        elif resposta == "2":
            print("consultar")
        elif resposta == "0":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida! Por favor, tente novamente.")

if __name__ == "__main__":
    main()
