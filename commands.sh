#!/bin/bash
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
az webapp up --sku F1 -n azure-cicd-pipeline --location westus2
