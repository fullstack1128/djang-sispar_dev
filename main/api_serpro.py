import re

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests.auth import HTTPBasicAuth


class APISerpro:
    ERROS_DE_API = {
        "sistema_indisponivel": "Sistema temporariamente indisponível, problemas no token.",
        "autenticacao_falha": "Erro ao se autenticar na API, o token é inválido após ser re-gerado.",
        "erro_call": "Erro ao fazer uma call para a API.",
    }
    token = None

    def __init__(self, *args, **kwargs):
        # Valida os dados de autenticação na API
        self.consumer_key = '8btcs5v1n76oadKhDDdMsepPvp8a'#settings.API_SERPRO_CONSUMER_KEY
        self.secret_key = 'eE7XabS8Yj2uzxiEvrlLxrhcLyEa'#settings.API_SERPRO_SECRET_KEY
        self.versao_api = '1'#settings.API_SERPRO_VERSION
        if not self.consumer_key or not self.secret_key:
            raise ImproperlyConfigured(
                "A consumer e a secret keys devem ser setadas através de variável de ambiente."
            )

    def get_token(self):
        url = settings.API_SERPRO_TOKEN_URL
        auth = HTTPBasicAuth(self.consumer_key, self.secret_key)
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, data, headers=header, auth=auth)
        token = response.json().get("access_token", None)
        if not token:
            raise ImproperlyConfigured(
                "Houve um erro ao autorizar o usuário na SERPRO com as informações forncecidas."
            )
        self.token = token
        return token

    def consulta_dividas_pelo_cnpj(self, cnpj, *args, **kwargs):
        numero_inscricao_devedor = re.sub(r"\D", "", str(cnpj))
        url = f"https://gateway.apiserpro.serpro.gov.br/consulta-divida-ativa-df/api/v{self.versao_api}/devedor/{numero_inscricao_devedor}"
        if not self.token:
            self.get_token()
        response = requests.get(url, headers={"Authorization": f"Bearer {self.token}"})
        # Token inválido, gerar novo token e tentar novamente
        if response.status_code == 401:
            self.token = self.get_token()
            if not kwargs.get("ja_tentou", False):
                self.consulta_dividas_pelo_cnpj(cnpj, ja_tentou=True)
            else:
                raise Exception(self.ERROS_DE_API["autenticacao_falha"])
        elif response.status_code == 403:
            raise Exception(self.ERROS_DE_API["sistema_indisponivel"])
        elif response.status_code == 500:
            raise Exception(self.ERROS_DE_API["erro_call"])
        elif response.status_code == 400:
            return None
        elif response.status_code == 404:
            return None
        data_to_return = [
            item for item in response.json() if "ATIVA" in item.get("situacaoDescricao")
        ]
        return data_to_return
