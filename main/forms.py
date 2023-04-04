from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms


class SearchForm(forms.Form):
    cnpj = forms.CharField(label="CNPJ", max_length=18)
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label="'")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("cnpj", css_class=""),
            Field("captcha"),
            Submit("submit_my_form", "Consultar", css_class="site-btn w-100"),
        )
        self.helper.form_show_labels = False
        self.helper.form_method = "GET"
        self.helper.form_action = "search"
