from pydantic import BaseModel
from pydantic_br import CNPJDigits, CPFDigits


class NovoCliente(BaseModel):
    id: CPFDigits | CNPJDigits
