import os
import base64
import sqlite3
from campanha import Campanha
from rede_social import RedeSocial, TODAS_REDES

class Usuario:
    def __init__(self, email: str, senha: str):
        chave_acesso = base64.b64encode(
            bytes(senha, "utf-8")
        ).decode("utf-8")
        pasta = f'c:/users/julio/sandbox/{email}'
        arquivo = os.path.join(pasta, chave_acesso)
        if not os.path.isdir(pasta):
            os.mkdir(pasta)  # No primeiro acesso, monta o ambiente para o usuário...
            self.con = sqlite3.connect(arquivo)
            for classe in [Campanha, RedeSocial]:
                classe.cria_tabela(self.con)            
        elif not os.path.isfile(arquivo):
            raise Exception("Usuário não encontrado")
        else:
            self.con = sqlite3.connect(arquivo)

    def campanhas(self, nome: str, redes: list) -> list:
        return [Campanha(nome, RedeSocial(r, self.con), self.con) for r in redes]


print('\n'.join(str(c) for c in Usuario(
        'julio.cascalles@python-brasil.com.br',
        'versão3-11.a7'
    ).campanhas('Promoção XYZ!', TODAS_REDES)
))
