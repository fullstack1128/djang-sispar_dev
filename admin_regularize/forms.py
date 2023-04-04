import datetime

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from localflavor.br.forms import BRCNPJField

from admin_regularize.utils import gerar_senha
from main.validators import validar_extensao


class AdminLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AdminLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <label for="id_username" class="form-label requiredField">
                        Username 
                    </label>
                    <div class="fieldbx">
                        <input type="text" name="username" placeholder="Username" autocapitalize="none" autocomplete="username" maxlength="150" class="textinput form-control" required id="id_username">
                        <i class="fal fa-envelope fa-fw"></i>
                    </div> 
                    """
                ),
                css_class="form-group",
            ),
            Div(
                HTML(
                    """
                    <label for="id_password" class="form-label requiredField">
                        Senha
                    </label>
                    <div class="fieldbx">
                        <input type="password" name="password" placeholder="Password" class="passwordinput form-control" required id="id_password"> 
                        <i class="far fa-lock fa-fw"></i>
                    </div> 
                    """
                ),
                css_class="form-group",
            ),
            Submit("submit", "LOGIN", css_class="btn-main"),
        )

    username = UsernameField(
        label="Username", widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        label="Senha", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


class FaturaFormBase(forms.Form):
    cnpj = BRCNPJField()
    empresa = forms.CharField()
    email = forms.EmailField()
    senha = forms.CharField(
        initial=gerar_senha(), widget=forms.PasswordInput(render_value=True)
    )
    valor = forms.DecimalField(min_value=0, max_digits=14, decimal_places=2)
    desconto = forms.DecimalField(
        min_value=0,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    inscricao = forms.CharField()
    data_apuracao = forms.DateField(
        initial=datetime.date.today() + datetime.timedelta(days=1),
        widget=forms.DateInput(attrs={"format": "dd/MM/yyyy"}),
    )
    banco = forms.CharField()
    A_VISTA = [(True, "Sim"), (False, "Não")]
    is_a_vista = forms.ChoiceField(choices=A_VISTA, widget=forms.RadioSelect())
    valor_entrada = forms.DecimalField(
        min_value=0, max_digits=14, decimal_places=2, required=False
    )
    numero_parcelas = forms.IntegerField(min_value=1, required=False)
    arquivo = forms.FileField(
        validators=[validar_extensao], widget=forms.FileInput(attrs={"accept": ".pdf"})
    )

    def __init__(self, *args, **kwargs):
        super(FaturaFormBase, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field("cnpj", placeholder="CNPJ", wrapper_class="fieldbx"),
                css_class="form-group",
            ),
            Div(
                Field(
                    "empresa",
                    placeholder="Nome da empresa",
                    wrapper_class="fieldbx",
                    id="empresa",
                ),
                css_class="form-group",
            ),
            Div(
                Field("email", placeholder="E-mail", wrapper_class="fieldbx"),
                css_class="form-group",
            ),
            Div(
                PrependedText(
                    "senha",
                    mark_safe(
                        '<span class="fas fa-eye-slash" style="cursor: pointer; align: right" id="eye"></span>'
                    ),
                    placeholder="Senha",
                    id="password",
                ),
                # HTML(
                #     """
                #     <div class="fieldbx">
                #         <input type="password" name="password" placeholder="Password" class="passwordinput form-control" required id="id_password">
                #         <i class="far fa-lock fa-fw" style="cursor: pointer; align: right"></i>
                #     </div>
                #     """
                # ),
                css_class="form-group",
            ),
            Div(
                Field(
                    "valor",
                    placeholder="Valor",
                    wrapper_class="fieldbx",
                    id="valor",
                ),
                css_class="form-group",
            ),
            Div(
                Field("desconto", placeholder="Desconto", wrapper_class="fieldbx"),
                css_class="form-group",
            ),
            Div(
                Field(
                    "inscricao",
                    placeholder="Inscrição",
                    wrapper_class="fieldbx",
                    id="inscricao",
                ),
                css_class="form-group",
            ),
            Div(
                Field(
                    "data_apuracao",
                    placeholder="Data de Apuração",
                    wrapper_class="form_group",
                ),
                css_class="form-group",
            ),
            Div(
                Field("banco", placeholder="Banco", wrapper_class="fieldbx"),
                css_class="form-group",
            ),
            Div(
                Div(
                    HTML("<h4>Valor a vista? </h4>"),
                    HTML(
                        """
                        <div class="radio-bx"> 
                            <input type="radio" class="form-check-input"  name="is_a_vista" value="True"  class="fieldbx" id="id_is_a_vista_0" required> 
                            <label for="id_is_a_vista_0" class="form-check-label">
                                Sim
                            </label> 
                        </div> 
                        <div class="radio-bx"> 
                            <input type="radio" class="form-check-input"  name="is_a_vista" value="False"  class="fieldbx" id="id_is_a_vista_1" required checked> 
                            <label for="id_is_a_vista_1" class="form-check-label">
                                Não
                            </label> 
                        </div>
                        """
                    ),
                    css_class="fieldbx radiorw",
                ),
                css_class="form-group",
            ),
            Div(
                Div(
                    Field(
                        "valor_entrada",
                        placeholder="Valor da Entrada",
                        wrapper_class="fieldbx",
                    ),
                    css_class="form-group",
                ),
                Div(
                    Field(
                        "numero_parcelas",
                        placeholder="Número de parcelas",
                        wrapper_class="fieldbx",
                    ),
                    css_class="form-group",
                ),
                css_id="parcelamento_fields",
            ),
            HTML(
                """
                <div class="form-group">
                    <div class="fieldbx">
                        <h6>Valor final: <span>R$ <span id="valor_final">0,00</span></span></h6>
                    </div>
                </div>
                """
            ),
            Div(
                Field(
                    "arquivo",
                    wrapper_class="fieldbx",
                ),
                css_class="form-group",
            ),
        )
        self.helper.form_show_labels = False


class CriarFaturaForm(FaturaFormBase):
    def __init__(self, *args, **kwargs):
        super(CriarFaturaForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit("submit", "CRIAR", css_class="btn-main"))


class EditarFaturaForm(FaturaFormBase):
    cnpj = BRCNPJField(required=False)
    empresa = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    senha = forms.CharField(widget=forms.PasswordInput(), required=False)
    valor = forms.DecimalField(
        min_value=0, max_digits=14, decimal_places=2, required=False
    )
    desconto = forms.DecimalField(
        min_value=0,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        required=False,
    )
    inscricao = forms.CharField()
    data_apuracao = forms.DateField(
        initial=datetime.date.today() + datetime.timedelta(days=1),
        widget=forms.DateInput(attrs={"format": "dd/MM/yyyy"}),
        required=False,
    )
    banco = forms.CharField(required=False)
    A_VISTA = [(True, "Sim"), (False, "Não")]
    is_a_vista = forms.ChoiceField(choices=A_VISTA, widget=forms.RadioSelect())
    arquivo = forms.FileField(
        validators=[validar_extensao],
        widget=forms.FileInput(attrs={"accept": ".pdf"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(EditarFaturaForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit("submit", "EDITAR", css_class="btn-main"))
