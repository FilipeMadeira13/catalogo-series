from typing import Annotated

from fastapi import Depends

from app.db.local import BancoDeDadosLocal
from app.repositories.serie_repositorio import SerieRepositorio


banco_de_dados = BancoDeDadosLocal()

def obter_banco_de_dados() -> BancoDeDadosLocal:
    return banco_de_dados

def obter_serie_repositorio(
        banco_de_dados_local: Annotated[
            BancoDeDadosLocal,
            Depends(obter_banco_de_dados)
        ]
) -> SerieRepositorio:
    return SerieRepositorio(banco_de_dados_local)