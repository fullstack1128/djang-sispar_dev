from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker

from auth_regularize.models import DadosUsuario, Usuario


class TestUsuario(TestCase):
    def test_criar_usuario(self):
        u = Usuario.objects.create(username="test", email="test@example.com")
        u.set_password("test")
        self.assertIsNone(u.full_clean())
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertTrue(u.check_password("test"))

    def test_criar_usuario_sem_senha(self):
        u = Usuario.objects.create(username="test")
        self.assertRaises(ValidationError, u.full_clean)

    def test_criar_dados_usuario(self):
        u = Usuario.objects.create(username="test")
        self.assertEqual(DadosUsuario.objects.count(), 1)
        self.assertEqual(DadosUsuario.objects.first().usuario, u)


class TestDadosUsuario(TestCase):
    def setUp(self):
        self.usuario = baker.make(Usuario)
        self.admin = baker.make(Usuario, is_staff=True, is_superuser=True)

    def test_atualizar_username(self):
        self.usuario.dados.cnpj = (
            "37.828.442/0001-30"  # CNPJ gerado no https://www.geradorcnpj.com/
        )
        self.usuario.dados.save()
        self.assertEqual(self.usuario.username, "37.828.442/0001-30")

    def test_nao_atualiza_username_admin(self):
        self.admin.dados.cnpj = (
            "71.651.293/0001-15"  # CNPJ gerado no https://www.geradorcnpj.com/
        )
        self.admin.dados.save()
        self.assertNotEqual(self.usuario.username, self.admin.dados.cnpj)
