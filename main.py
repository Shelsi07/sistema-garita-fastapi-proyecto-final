from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Body
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime
from correo import enviar_correo

from sqlalchemy.orm import Session

import models
import schemas
import crud
import os
import qrcode
import uuid


from database import engine, SessionLocal
from auth import create_token, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Garita Tecnológica"
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.post("/login/")
def login(datos: dict = Body(...)):

    correo = datos["correo"]
    contrasena = datos["contrasena"]

    if correo == "admin@gmail.com" and contrasena == "G1234*":

        return {
            "access_token": "token_prueba"
        }

    return {
        "error": "Credenciales incorrectas"
    }
    
@app.post("/registro/")
def registro(
    usuario: schemas.CrearUsuario,
    db: Session = Depends(get_db)
):

    return crud.create_user(db, usuario)


@app.post("/login/")
def login(
    datos: schemas.LoginUsuario,
    db: Session = Depends(get_db)
):

    usuario = crud.authenticate_user(
        db,
        datos.correo,
        datos.contrasena
    )

    if not usuario:

        raise HTTPException(
            status_code=400,
            detail="Credenciales incorrectas"
        )

    token = create_token({
        "sub": usuario.correo
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/protegido/")
def protegido(
    usuario: str = Depends(get_current_user)
):

    return {
        "mensaje": f"Bienvenido {usuario}"
    }


@app.post("/prerregistro/")
def prerregistro(
    datos: schemas.CrearPrerregistro,
    db: Session = Depends(get_db)
):

    return crud.crear_prerregistro(
        db,
        datos
    )

@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


@app.get("/visitantes", response_class=HTMLResponse)
def visitantes(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="visitantes.html"
    )


@app.get("/prerregistro", response_class=HTMLResponse)
def prerregistro(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="prerregistro.html"
    )

@app.post("/visitantes/")
def registrar_visitante(
    visitante: schemas.VisitanteCreate,
    db: Session = Depends(get_db)
):

    vecino = db.query(
        models.Vecino
    ).filter(

        models.Vecino.codigo_unico ==
        visitante.codigo_vecino

    ).first()

    if not vecino:

        return {
            "mensaje":
            "Código de vecino inválido"
        }

    nuevo = models.Visitante(

        nombre = visitante.nombre,

        dpi = visitante.dpi,

        placa = visitante.placa,

        codigo_vecino = visitante.codigo_vecino,

        vivienda = vecino.vivienda,

        fecha_ingreso = datetime.now()
    )

    db.add(nuevo)

    db.commit()

    db.refresh(nuevo)

    if vecino:

        enviar_correo(
            vecino.correo,
            visitante.nombre
        )

    return {
        "mensaje":
        "Visitante registrado correctamente"
    }

@app.post("/generar_qr/")
def generar_qr(datos: dict):

    contenido = f"""
    Nombre: {datos['nombre']}
    DPI: {datos['dpi']}
    Placa: {datos['placa']}
    """

    qr = qrcode.make(contenido)

    nombre_archivo = f"{datos['nombre']}.png"

    ruta = f"qrs/{nombre_archivo}"

    qr.save(ruta)

    return {
        "mensaje": "QR generado correctamente",
        "ruta": ruta
    }

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@app.post("/vecinos/")
def crear_vecino(
    vecino: dict,
    db: Session = Depends(get_db)
):

    nuevo = models.Vecino(

        nombre = vecino["nombre"],

        correo = vecino["correo"],

        codigo_unico = vecino["codigo_unico"],

        vivienda = vecino["vivienda"]
    )

    db.add(nuevo)

    db.commit()

    return {
        "mensaje": "Vecino creado"
    }

@app.put("/salida/{id}")
def registrar_salida(
    id: int,
    db: Session = Depends(get_db)
):

    visitante = db.query(
        models.Visitante
    ).filter(
        models.Visitante.id == id
    ).first()

    visitante.fecha_salida = datetime.now()

    db.commit()

    return {
        "mensaje": "Salida registrada"
    }

@app.get("/placa/{placa}")
def buscar_placa(
    placa: str,
    db: Session = Depends(get_db)
):

    visitante = db.query(
        models.Visitante
    ).filter(
        models.Visitante.placa == placa
    ).all()

    return visitante

@app.post("/prerregistro/")
def prerregistro(datos: dict):

    codigo = str(uuid.uuid4())

    qr = qrcode.make(codigo)

    qr.save(f"qrs/{codigo}.png")

    return {
        "codigo": codigo
    }

@app.get("/historial/")
def historial(
    db: Session = Depends(get_db)
):

    return db.query(
        models.Visitante
    ).all()

@app.get("/vecinos", response_class=HTMLResponse)
def vecinos_html(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="vecinos.html"
    )


@app.get("/historial", response_class=HTMLResponse)
def historial_html(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="historial.html"
    )


@app.get("/placas", response_class=HTMLResponse)
def placas_html(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="placas.html"
    )


@app.get("/salidas", response_class=HTMLResponse)
def salidas_html(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="salidas.html"
    )