import smtplib

from email.mime.text import MIMEText


def enviar_correo(destino, visitante):

    remitente = "TU_CORREO@gmail.com"

    password = "TU_PASSWORD_APP"

    mensaje = MIMEText(

        f"El visitante {visitante} ha llegado a la garita."
    )

    mensaje["Subject"] = "Nueva visita"

    mensaje["From"] = remitente

    mensaje["To"] = destino

    servidor = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    servidor.starttls()

    servidor.login(
        remitente,
        password
    )

    servidor.send_message(mensaje)

    servidor.quit()