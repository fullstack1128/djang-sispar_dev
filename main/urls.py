from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("usuario/home/", views.index_usuario, name="index_usuario"),
    path("usuario/fatura/<int:id>", views.download_fatura, name="download_fatura"),
]
