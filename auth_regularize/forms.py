from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(Field("username"), css_class="form-group"),
            Div(Field("password"), css_class="form-group"),
            Field("captcha"),
            Submit("submit_my_form", "CONTINUAR", css_class="btn-main"),
        )

    username = UsernameField(
        label="CPF / CNPJ",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu CPF/CNPJ"}),
        max_length=18,
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
            }
        ),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label="")
