TODAS_REDES = ['Facebook', 'Twitter', 'Instagram', 'Youtube', 'Linkedin']


class RedeSocial:
    def __init__(self, nome: str, conexao):
        cursor = conexao.execute('SELECT id FROM rede_social WHERE nome = ?', (nome,))
        dados = cursor.fetchone()
        if dados:
            self.id = dados[0]
        else:
            cursor = conexao.execute('INSERT INTO rede_social (nome) VALUES (?)', (nome,))
            conexao.commit()
            self.id = cursor.lastrowid
        self.nome = nome

    @staticmethod
    def cria_tabela(conexao):
        conexao.execute('''
        CREATE TABLE IF NOT EXISTS rede_social (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE
        )''')
        conexao.commit()
