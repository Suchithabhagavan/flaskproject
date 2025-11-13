# config.py
import os
import urllib.parse

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Flask secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    # Azure Blob Storage
    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or 'ENTER_STORAGE_ACCOUNT_NAME'
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or 'ENTER_BLOB_STORAGE_KEY'
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or 'ENTER_IMAGES_CONTAINER_NAME'

    # Azure SQL Database
    SQL_SERVER = os.environ.get('SQL_SERVER') or 'ENTER_SQL_SERVER_NAME.database.windows.net'
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'ENTER_SQL_DB_NAME'
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or 'ENTER_SQL_SERVER_USERNAME'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or 'ENTER_SQL_SERVER_PASSWORD'

    # Safely encode username and password for URI
    user_enc = urllib.parse.quote_plus(SQL_USER_NAME)
    pwd_enc = urllib.parse.quote_plus(SQL_PASSWORD)
    server = SQL_SERVER  # e.g. cms-sql-server.database.windows.net

    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{user_enc}:{pwd_enc}@{server}:1433/{SQL_DATABASE}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Microsoft Authentication (MSAL)
    CLIENT_ID = os.environ.get('CLIENT_ID') or 'ENTER_CLIENT_ID_HERE'
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or 'ENTER_CLIENT_SECRET_HERE'
    TENANT_ID = os.environ.get('TENANT_ID') or ''
    AUTHORITY = (
        f"https://login.microsoftonline.com/{TENANT_ID}"
        if TENANT_ID else "https://login.microsoftonline.com/common"
    )

    REDIRECT_PATH = "/getAToken"  # must match the redirect URI in Entra ID
    SCOPE = ["User.Read"]         # minimal required permission
    SESSION_TYPE = "filesystem"   # for storing MSAL session tokens
