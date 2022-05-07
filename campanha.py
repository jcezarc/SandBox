from random import randint
from rede_social import RedeSocial

class Campanha:
    def __init__(self, nome: str, rede_social: RedeSocial, conexao):
        dados = conexao.execute('''
            SELECT id, ativa, rede_social_id,
            reacoes_positivas, reacoes_negativas
            FROM campanha WHERE nome = ? AND rede_social_id = ?
        ''', (nome, rede_social.id,)).fetchone()
        if dados is None:
            pos, neg = [randint(0, 100) for _ in range(2)]
            cursor = conexao.execute('''
                INSERT INTO campanha (
                    nome, ativa, rede_social_id,
                    reacoes_positivas, reacoes_negativas
                )VALUES (?, 1, ?, ?, ?)
            ''', (nome, rede_social.id, pos, neg,))
            conexao.commit()
            dados = [cursor.lastrowid, True, rede_social.id, pos, neg]
        self.nome = f'{nome} - {rede_social.nome}'
        self.id, self.ativa, self.rede_id, *self.reacoes = dados

    @staticmethod
    def cria_tabela(conexao):
        conexao.execute('''
        CREATE TABLE IF NOT EXISTS campanha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ativa BOOLEAN, rede_social_id INTEGER,
            reacoes_positivas INTEGER,
            reacoes_negativas INTEGER,
            FOREIGN KEY (rede_social_id) REFERENCES rede_social(id)
        )''')
        conexao.commit()

    def __str__(self):
        return '{} = pos:{}, neg:{}'.format(
            self.nome, self.reacoes[0], self.reacoes[1]
        )
