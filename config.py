import os

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root123")
DB_NAME = os.environ.get("DB_NAME", "eduvision")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
SECRET_KEY = os.environ.get("SECRET_KEY", "eduvision-secret-key")
