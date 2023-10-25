@echo off
python -m venv env && .\env\Scripts\activate && pip install -r req.txt && alembic revision --autogenerate -m "database creation"