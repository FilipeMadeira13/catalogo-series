import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from filelock import FileLock
from app.models.serie import Serie, SerieCriarAtualizar, SerieResposta
from app.utils.json_atomico import salvar_json_atomico

router = APIRouter(
    prefix='/series'
)

ARQUIVO = Path('series.json')
LOCK = FileLock(str(ARQUIVO) + '.lock')

@router.post('/', response_model=SerieResposta, status_code=201, tags=['Serie'])
def criar_serie(serie: SerieCriarAtualizar):
    with LOCK:
        try:
            with ARQUIVO.open('r', encoding='utf-8') as arquivo:
                series = json.load(arquivo)
        except FileNotFoundError:
            series = []

        for serie_existente in series:
            if (
                serie_existente['titulo'].strip().casefold()
                ==  serie.titulo.strip().casefold()
            ):
                raise HTTPException(
                    status_code=409,
                    detail='Esta série já está cadastrada.'
                )

        novo_id = max(
            (s['id'] for s in series),
            default=0
        ) + 1

        nova_serie = Serie(
            id=novo_id,
            **serie.model_dump(),
        )

        series.append(nova_serie.model_dump())

        salvar_json_atomico(ARQUIVO, series)

        return {
            'mensagem': 'Série cadastrada com sucesso!',
            'serie': nova_serie,
        }