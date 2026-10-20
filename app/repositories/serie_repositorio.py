import sqlite3
from typing import Optional

from app.db.local import BancoDeDadosLocal
from app.models.serie import Serie, SerieCriarAtualizar, SerieResposta
from app.utils.normalizacao import normalizar_titulo


class SerieRepositorio:
    def __init__(self, database: BancoDeDadosLocal) -> None:
        self.db = database

    async def listar_series(self) -> list[Serie]:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                '''
                SELECT id, titulo, genero, ano_lancamento, temporadas
                FROM series
                '''
            )
            linhas = cursor.fetchall()
            return [
                Serie(
                    id=linha[0],
                    titulo=linha[1],
                    genero=linha[2],
                    ano_lancamento=linha[3],
                    temporadas=linha[4],
                ) for linha in linhas
            ]




    async def obter_serie(self, titulo: str) -> Optional[Serie]:
        titulo_normalizado = normalizar_titulo(titulo)

        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                '''
                SELECT id, titulo, genero, ano_lancamento, temporadas
                FROM series
                WHERE titulo_normalizado = ?
                ''', (titulo_normalizado,)

            )
            linha = cursor.fetchone()

            if linha:
                return Serie(
                    id=linha[0],
                    titulo=linha[1],
                    genero=linha[2],
                    ano_lancamento=linha[3],
                    temporadas=linha[4],
                )

    async def criar_serie(self, serie: SerieCriarAtualizar) -> Optional[SerieResposta]:
        titulo = serie.titulo.strip()
        titulo_normalizado = titulo.casefold()

        if not titulo_normalizado:
            raise ValueError('O título não pode ser vazio')


        try:
            with self.db.conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    '''
                    INSERT INTO series
                    (
                    titulo,
                    titulo_normalizado,
                    genero,
                    ano_lancamento,
                    temporadas
                    )
                    VALUES (?, ?, ?, ?, ?)
                    ''', (titulo, titulo_normalizado, serie.genero, serie.ano_lancamento, serie.temporadas)
                )
                novo_id = cursor.lastrowid
                if novo_id:
                    nova_serie = Serie(
                        id=novo_id,
                        titulo=titulo,
                        genero=serie.genero,
                        ano_lancamento=serie.ano_lancamento,
                        temporadas=serie.temporadas,
                    )
                    return SerieResposta(
                        mensagem='Série criada com sucesso',
                        serie=nova_serie,
                    )
        except sqlite3.IntegrityError as erro:
            if (
                erro.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE"
                and 'series.titulo_normalizado' in str(erro)
            ):
                raise ValueError("Já existe uma série cadastrada com esse título") from erro
            raise
