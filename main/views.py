import logging

from django.contrib.auth.decorators import login_required
from django.http.response import (
    FileResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.shortcuts import redirect, render
from django.urls import reverse

from .api_serpro import APISerpro
from .forms import SearchForm
from .models import Fatura

api_serpro = APISerpro()

logger = logging.getLogger(__name__)


def index(request):
    context = {"form": SearchForm()}
    return render(request, "main/index.html", context=context)


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        cnpj = request.GET.get("cnpj", None)
        dividas = None
        if cnpj:
            try:
                dividas = api_serpro.consulta_dividas_pelo_cnpj(cnpj)
            except Exception as e:
                logger.exception(e)
                return HttpResponseServerError(
                    render(
                        request,
                        "main/error.html",
                        context={
                            "mensagem": "Erro ao se conectar com a API de consulta."
                        },
                    )
                )
        if len(dividas) == 0:
            return HttpResponseNotFound(
                render(
                    request,
                    "main/error.html",
                    context={"mensagem": "Nenhum registro foi encontrado"},
                )
            )
        context = {"dividas": dividas}
        return render(request, "main/search.html", context=context)
    else:
        return redirect(reverse("index"))


@login_required(login_url="/auth/login/")
def index_usuario(request):
    context = {}
    try:
        fatura = Fatura.objects.get(empresa=request.user)
        context["saldo_devedor"] = fatura.saldo_devedor
    except Fatura.DoesNotExist:
        fatura = None
    context["fatura"] = fatura
    return render(request, "main/home_user.html", context)


@login_required(login_url="/auth/login/")
def download_fatura(request, id=None):
    try:
        fatura = Fatura.objects.get(id=id)
    except Fatura.DoesNotExist:
        return HttpResponseNotFound(
            render(
                request,
                "main/error.html",
                context={"mensagem": "A fatura não foi encontrada"},
            )
        )
    if request.user != fatura.empresa:
        return HttpResponseForbidden(
            request,
            "main/error.html",
            context={"mensagem": "Você não tem autorização para acessar esta página"},
        )
    return FileResponse(fatura.arquivo, as_attachment=True)


def not_found(request, exception):
    return HttpResponseNotFound(
        render(
            request,
            "main/error.html",
            context={"mensagem": exception.message},
        )
    )
