from django.contrib.auth import views as dj_auth_views
from django.urls import path

from . import views
from .forms import AdminLoginForm

urlpatterns = [
    path("", views.index, name="admin_index"),
    path("criar-fatura/", views.criar_fatura, name="admin_criar_fatura"),
    path("consulta-cnpj/", views.consulta_cnpj, name="admin_consulta_cnpj"),
    path("fatura/<int:id>/delete", views.delete_fatura, name="admin_delete_fatura"),
    path("fatura/<int:id>/editar", views.editar_fatura, name="admin_editar_fatura"),
    path(
        "login/",
        dj_auth_views.LoginView.as_view(
            template_name="admin_regularize/login.html",
            authentication_form=AdminLoginForm,
            next_page="/admin/",
            redirect_authenticated_user=True,
        ),
        name="admin_login",
    ),
]
