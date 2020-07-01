import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Спорим_что_ты_не_угадаешь'