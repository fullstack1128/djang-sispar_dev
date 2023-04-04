from django.core.exceptions import ValidationError


def validar_extensao(value):
    if not value.name.endswith(".pdf"):
        raise ValidationError("A Fatura deve ser um arquivo pdf.")
