from pydantic import BaseModel, Field, field_validator


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

    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, valor: str) -> str:
        titulo = valor.strip()

        if not titulo:
            raise ValueError('O título não pode estar vazio')

        return titulo


class SerieResposta(BaseModel):
    mensagem: str
    serie: Serie