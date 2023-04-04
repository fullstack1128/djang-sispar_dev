from django.contrib.auth import views as dj_auth_views
from django.urls import path

from .forms import LoginForm

urlpatterns = [
    path(
        "login/",
        dj_auth_views.LoginView.as_view(
            template_name="auth_regularize/login.html",
            authentication_form=LoginForm,
            next_page="/usuario/home/",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        dj_auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),
]
