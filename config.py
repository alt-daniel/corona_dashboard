import os

class Config:
    SECRET_KEY = 'mdfjaggjh'
    FLASK_ENVIRONMENT = ''

    # DB credentials
    DB_USERNAME = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_SCHEMA = ''

    # Static
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(ROOT_DIR, "dashboard_app/static")