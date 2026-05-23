from sqlalchemy.orm import Session
import models
import random
import string
import qrcode

from auth import hash_password, verify_password


def generar_codigo():

    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )


def create_user(db: Session, usuario):

    hashed = hash_password(usuario.contrasena)

    db_user = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contrasena=hashed
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(
    db: Session,
    correo,
    contrasena
):

    user = db.query(models.Usuario).filter(
        models.Usuario.correo == correo
    ).first()

    if not user:
        return None

    if not verify_password(
        contrasena,
        user.contrasena
    ):
        return None

    return user


def create_vecino(db: Session, vecino):

    codigo = generar_codigo()

    nuevo_vecino = models.Vecino(
        nombre=vecino.nombre,
        correo=vecino.correo,
        vivienda_id=vecino.vivienda_id,
        codigo_unico=codigo
    )

    db.add(nuevo_vecino)
    db.commit()
    db.refresh(nuevo_vecino)

    return nuevo_vecino

def crear_prerregistro(
    db: Session,
    datos
):

    contenido_qr = f"""
    Visitante: {datos.visitante_nombre}
    DPI: {datos.dpi}
    Placa: {datos.placa}
    """

    img = qrcode.make(contenido_qr)

    nombre_archivo = f"qr_{datos.visitante_nombre}.png"

    img.save(nombre_archivo)

    nuevo = models.Prerregistro(
        visitante_nombre=datos.visitante_nombre,
        dpi=datos.dpi,
        placa=datos.placa,
        vecino_id=datos.vecino_id,
        codigo_qr=nombre_archivo
    )

    db.add(nuevo)

    db.commit()

    db.refresh(nuevo)

    return nuevo

def crear_visitante(db: Session, visitante):

    nuevo = models.Visitante(

        nombre=visitante.nombre,

        dpi=visitante.dpi,

        placa=visitante.placa,

        codigo_vecino=visitante.codigo_vecino
    )

    db.add(nuevo)

    db.commit()

    db.refresh(nuevo)

    return nuevo