from django.contrib.auth import get_user_model
from django.db import models

from .validators import validar_extensao

Usuario = get_user_model()


class Fatura(models.Model):
    empresa = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    # Valor máximo: 999.999.999.999,99 (novecentos e noventa e nove bilhões)
    # A maior dívida fiscal com a União era R$7,7 bi em 2021, então esse valor é razoável.
    # Fonte: https://congressoemfoco.uol.com.br/area/pais/saiba-quais-sao-as-dez-as-empresas-que-mais-devem-aos-cofres-publicos/
    valor = models.DecimalField(max_digits=14, decimal_places=2)
    desconto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    inscricao = models.CharField(max_length=255, unique=True)
    data_apuracao = models.DateField()
    banco = models.CharField(max_length=255)
    is_a_vista = models.BooleanField(default=True)
    entrada = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    numero_parcelas = models.SmallIntegerField(null=True, blank=True)
    arquivo = models.FileField(upload_to="faturas/", validators=[validar_extensao])

    @property
    def saldo_devedor(self):
        return round(self.valor - (self.desconto / 100 * self.valor), 2)
