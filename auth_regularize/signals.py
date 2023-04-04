from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DadosUsuario, Usuario


@receiver(post_save, sender=Usuario)
def criar_dados_usuario(sender, instance, created, **kwargs):
    if created:
        DadosUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=DadosUsuario)
def atualizar_username(sender, instance, created, **kwargs):
    if instance.cnpj and not instance.usuario.is_staff:
        instance.usuario.username = instance.cnpj
        instance.usuario.clean()
        instance.usuario.save()