import os
import random
import string

from django.contrib.auth import get_user_model
from django.template.loader import get_template

Usuario = get_user_model()


def gerar_senha(tamanho=15):
    caracteres = [string.ascii_letters, string.digits, "!$()?=^;:,."]
    random.seed = os.urandom(1024)

    return "".join(random.choice(random.choice(caracteres)) for i in range(tamanho))


def enviar_email_fatura(usuario: Usuario, empresa: dict, senha: str):
    text = get_template("admin_regularize/mail.txt")
    html = get_template("admin_regularize/mail.html")
    context = {"empresa": empresa, "senha": senha}

    text_content = text.render(context)
    html_content = html.render(context)

    return usuario.email_user(
        "Conta criada com sucesso!", text_content, html_message=html_content
    )
