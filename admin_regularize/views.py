import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http.response import (
    HttpResponseNotFound,
    HttpResponseRedirect,
    HttpResponseServerError,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse

from admin_regularize.utils import enviar_email_fatura
from main.api_serpro import APISerpro
from main.models import Fatura

from .forms import CriarFaturaForm, EditarFaturaForm

Usuario = get_user_model()

api_serpro = APISerpro()

logger = logging.getLogger(__name__)


def user_is_staff(user):
    return user.is_staff


LOGIN_REQUIRED_KWARGS = {"login_url": "/admin/login/"}
USER_PASSES_TEST_KWARGS = {"test_func": user_is_staff, "login_url": "/admin/login/"}


@login_required(**LOGIN_REQUIRED_KWARGS)
@user_passes_test(**USER_PASSES_TEST_KWARGS)
def index(request):
    filter_str = request.GET.get("filter", "")
    faturas = Fatura.objects.filter(
        Q(empresa__dados__nome__icontains=filter_str)
        | Q(empresa__email__icontains=filter_str)
        | Q(data_apuracao__icontains=filter_str)
        | Q(valor__icontains=filter_str)
        | Q(empresa__username__icontains=filter_str)
    )
    paginator = Paginator(faturas, 10)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)
    context = {
        "usuarios": faturas.count(),
        "faturas": [
            {
                "id": item.id,
                "cnpj": item.empresa.username,
                "email": item.empresa.email,
                "data": item.data_apuracao,
                "valor": item.valor,
            }
            for item in page_obj.object_list
        ],
        "page": {
            "object": page_obj,
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "list": paginator.get_elided_page_range(
                page_obj.number, on_each_side=1, on_ends=3
            ),
        },
    }
    return render(request, "admin_regularize/index.html", context=context)


@login_required(**LOGIN_REQUIRED_KWARGS)
@user_passes_test(**USER_PASSES_TEST_KWARGS)
def criar_fatura(request):
    if request.method == "POST":
        form = CriarFaturaForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form_data = form.cleaned_data
            empresa = Usuario.objects.get_or_create(username=form_data["cnpj"])
            # get_or_create() retorna um tuple onde o objeto [1] é um booleano
            # se o objeto foi criado, então se a empresa for criada, salva os dados
            # dela no banco de dados.
            empresa[0].dados.cnpj = form_data["cnpj"]
            empresa[0].dados.nome = form_data["empresa"]
            empresa[0].email = form_data["email"]
            empresa[0].set_password(form_data["senha"])
            empresa[0].save()
            empresa[0].dados.save()
            enviar_email_fatura(
                empresa[0],
                {"nome": form_data["empresa"], "cnpj": form_data["cnpj"]},
                form_data["senha"],
            )

            dados_fatura = {
                "empresa": empresa[0],
                "valor": form_data["valor"],
                "desconto": form_data["desconto"],
                "inscricao": form_data["inscricao"],
                "data_apuracao": form_data["data_apuracao"],
                "banco": form_data["banco"],
                "is_a_vista": form_data["is_a_vista"],
                "entrada": form_data["valor_entrada"],
                "numero_parcelas": form_data["numero_parcelas"],
                "arquivo": form_data["arquivo"],
            }

            Fatura.objects.create(**dados_fatura)

            return HttpResponseRedirect(reverse("admin_index"))

    else:
        form = CriarFaturaForm()

    return render(request, "admin_regularize/criar_fatura.html", {"form": form})


@login_required(**LOGIN_REQUIRED_KWARGS)
@user_passes_test(**USER_PASSES_TEST_KWARGS)
def editar_fatura(request, id):
    try:
        fatura = Fatura.objects.get(id=id)
    except Fatura.DoesNotExist:
        return HttpResponseNotFound("Fatura não encontrada.")
    if request.method == "PATCH":
        form = EditarFaturaForm(request.PATCH, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data

            senha = form_data.get("senha", None)
            if senha:
                fatura.empresa.set_password(senha)

            fatura.empresa.dados.cnpj = form_data.get("cnpj", fatura.empresa.dados.cnpj)
            fatura.empresa.dados.nome = form_data.get(
                "empresa", fatura.empresa.dados.nome
            )
            fatura.empresa.email = form_data.get("email", fatura.empresa.email)
            fatura.empresa.save()

            fatura.valor = form_data.get("valor", fatura.valor)
            fatura.desconto = form_data.get("desconto", fatura.desconto)
            fatura.inscricao = form_data.get("inscricao", fatura.inscricao)
            fatura.data_apuracao = form_data.get("data_apuracao", fatura.data_apuracao)
            fatura.banco = form_data.get("banco", fatura.banco)
            fatura.is_a_vista = form_data.get("is_a_vista", fatura.is_a_vista)
            fatura.entrada = form_data.get("valor_entrada", fatura.entrada)
            fatura.numero_parcelas = form_data.get(
                "numero_parcelas", fatura.numero_parcelas
            )
            fatura.arquivo = form_data.get("arquivo", fatura.arquivo)

            fatura.save()

            return HttpResponseRedirect(reverse("admin_index"))

    else:
        form_data = {
            "cnpj": fatura.empresa.dados.cnpj,
            "empresa": fatura.empresa.dados.nome,
            "email": fatura.empresa.email,
            "senha": "qualquer_coisa",
            "valor": fatura.valor,
            "desconto": fatura.desconto,
            "inscricao": fatura.inscricao,
            "data_apuracao": fatura.data_apuracao,
            "banco": fatura.banco,
            "valor_entrada": fatura.entrada,
            "numero_parcelas": fatura.numero_parcelas,
        }
        form = EditarFaturaForm(form_data)

    return render(request, "admin_regularize/criar_fatura.html", {"form": form})


@login_required(**LOGIN_REQUIRED_KWARGS)
@user_passes_test(**USER_PASSES_TEST_KWARGS)
def delete_fatura(request, id):
    try:
        fatura = Fatura.objects.get(id=id)
    except Fatura.DoesNotExist:
        return HttpResponseRedirect("/admin/")
    else:
        usuario = fatura.empresa
        fatura.delete()
        usuario.delete()
        return HttpResponseRedirect("/admin/")


@login_required(**LOGIN_REQUIRED_KWARGS)
@user_passes_test(**USER_PASSES_TEST_KWARGS)
def consulta_cnpj(request):
    cnpj = request.GET.get("cnpj", None)
    try:
        dividas = api_serpro.consulta_dividas_pelo_cnpj(cnpj)
    except Exception as e:
        logger.exception(e)
        return HttpResponseServerError(
            "Não foi possível completar a sua request neste momento."
        )
    if cnpj:
        return JsonResponse(dividas, safe=False)
    return HttpResponseNotFound("Não foi posível achar o CNPJ informado.")
