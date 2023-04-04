#!/bin/bash
# Criar um ambiente virtual
python -m venv venv
# Ativa o ambiente virtual
source venv/bin/activate
# Instala os requerimentos
pip install -r requirements.txt
# Migra o DB
python manage.py migrate
# Cria um super usuário
python manage.py createsuperuser
# Ativa o servidor
python manage.py runserver