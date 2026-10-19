from pydantic import BaseModel, Field


class Serie(BaseModel):
    id: int
    titulo: str
    genero: str
    ano_lancamento: int = Field(gt=1900)
    temporadas: int = Field(gt=0)


class SerieCriarAtualizar(BaseModel):
    titulo: str
    genero: str
    ano_lancamento: int = Field(gt=1900)
    temporadas: int = Field(gt=0)


class SerieResposta(BaseModel):
    mensagem: str
    serie: Serie