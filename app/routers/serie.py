from pathlib import Path
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from filelock import FileLock
from app.dependencias import obter_serie_repositorio
from app.models.serie import Serie, SerieCriarAtualizar, SerieResposta
from app.repositories.serie_repositorio import SerieRepositorio
from app.utils.utils_json import carregar_json, salvar_json_atomico

router = APIRouter(
    prefix='/series'
)

ARQUIVO = Path('series.json')
LOCK = FileLock(str(ARQUIVO) + '.lock')

@router.get('/', response_model=list[Serie], tags=['Serie'])
def listar_series(serie_repositorio: Annotated[SerieRepositorio, Depends(obter_serie_repositorio)]):
    return serie_repositorio.listar_series()

@router.get('/{titulo}', response_model=Optional[Serie], tags=['Serie'])
def obter_serie(
    serie_repositorio: Annotated[SerieRepositorio, Depends(obter_serie_repositorio)],
    titulo: str,
):
    serie = serie_repositorio.obter_serie(titulo)
    if not serie:
        raise HTTPException(
            status_code=404,
            detail='Série não encontrada.'
        )
    return serie


@router.post('/', response_model=SerieResposta, status_code=201, tags=['Serie'])
def criar_serie(
    serie: SerieCriarAtualizar,
    serie_repositorio: Annotated[SerieRepositorio, Depends(obter_serie_repositorio)],
    ):
        try:
            return serie_repositorio.criar_serie(serie)
        except ValueError as erro:
            if str(erro) == "Já existe uma série cadastrada com esse título":
                raise HTTPException(
                    status_code=409,
                    detail=str(erro)
                ) from erro
            raise