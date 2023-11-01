#! /bin/bash
python3 -m venv env
source env/bin/activate
pip install -r req.txt
alembic revision --autogenerate -m "database creation"
alembic upgrade head