from contextlib import contextmanager
import sqlite3

class BancoDeDadosLocal():
    def __init__(self, nome_arquivo='series.db') -> None:
        self.nome_arquivo = nome_arquivo
        self.inicializar_banco()

    @contextmanager
    def conectar(self):
        conexao = sqlite3.connect(self.nome_arquivo)
        try:
            yield conexao
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def inicializar_banco(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS series (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    titulo_normalizado TEXT NOT NULL UNIQUE,
                    genero TEXT NOT NULL,
                    ano_lancamento INTEGER NOT NULL,
                    temporadas INTEGER NOT NULL
                )
            ''')