from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True)
    contrasena = Column(String)
    rol_id = Column(Integer, nullable=True)


class Vecino(Base):

    __tablename__ = "vecinos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String)
    codigo_unico = Column(String)
    vivienda = Column(String)


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    visitante_id = Column(Integer)
    vecino_id = Column(Integer)
    tipo_ingreso = Column(String)
    fecha_ingreso = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_salida = Column(TIMESTAMP, nullable=True)
    agente = Column(String)

class Prerregistro(Base):

    __tablename__ = "prerregistros"

    id = Column(Integer, primary_key=True, index=True)
    nombre_visitante = Column(String)
    dpi = Column(String)
    placa = Column(String)
    codigo_qr = Column(String)
    vivienda = Column(String)

class Visitante(Base):

    __tablename__ = "visitantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    dpi = Column(String)
    placa = Column(String)
    codigo_vecino = Column(String)
    vivienda = Column(String)
    fecha_ingreso = Column(DateTime)
    fecha_salida = Column(DateTime, nullable=True)