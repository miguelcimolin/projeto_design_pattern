import sqlite3

class Order:
    def __init__(self, order_id, db_path="./bd/banco.db"):
        self.order_id = order_id
        self.state = None
        self.observers = []
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Cria a tabela no banco de dados, se ela não existir."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ordem (
                id TEXT PRIMARY KEY,
                sequencial INTEGER,
                nome_cliente TEXT,
                cpf_cliente TEXT,
                data_compra DATE,
                estado TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _persist_final_state(self):
        """Persiste o estado final 'Completed' no banco de dados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("UPDATE ordem SET estado = ? WHERE id = ?", ("Completed", self.order_id))

        conn.commit()
        conn.close()

    def complete_order(self):
        """Finaliza o pedido sem definir o estado como None."""
        self.state = None
        self._persist_final_state()
        print(f"Pedido {self.order_id} foi finalizado e registrado como 'Completed' no banco de dados.")
        self.notify_observers()

    def _persist_state(self):
        """Persiste o estado atual no banco de dados."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Tenta inserir o ID e o estado, respeitando a unicidade do ID
            cursor.execute("INSERT INTO ordem (id, estado) VALUES (?, ?)", (self.order_id, self.state.__class__.__name__))
        except sqlite3.IntegrityError:
            # ID já existe, atualiza o estado
            cursor.execute("UPDATE ordem SET estado = ? WHERE id = ?", (self.state.__class__.__name__, self.order_id))

        conn.commit()
        conn.close()

    def set_state(self, state):
        """Define o novo estado e notifica os observadores."""
        self.state = state
        self._persist_state()  # Persiste o estado no banco de dados
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        if self.state is None:
            print(f"Pedido {self.order_id} não tem mais estados para processar. Notificações encerradas.")
            return
        for observer in self.observers:
            observer.update(self)

    def start_processing(self):
        if self.state:
            self.state.handle(self)
