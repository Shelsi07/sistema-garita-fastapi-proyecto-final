from pydantic import BaseModel


class CrearUsuario(BaseModel):
    nombre: str
    correo: str
    contrasena: str


class LoginUsuario(BaseModel):
    correo: str
    contrasena: str


class CrearVecino(BaseModel):
    nombre: str
    correo: str
    vivienda_id: int


class CrearVisitante(BaseModel):
    nombre: str
    dpi: str
    placa: str


class CrearVisita(BaseModel):
    visitante_id: int
    vecino_id: int
    tipo_ingreso: str
    agente: str


class CrearPrerregistro(BaseModel):

    visitante_nombre: str
    dpi: str
    placa: str
    vecino_id: int

class VisitanteCreate(BaseModel):

    nombre: str

    dpi: str

    placa: str

    codigo_vecino: str