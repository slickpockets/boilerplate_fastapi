from dotenv import dotenv_values
from typing import Optional

from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.applications import Starlette
from pathlib import Path
from fastapi_mail import ConnectionConfig
from models.Utils import setupdb
from logconfig import debugLogger, errorLogger, infoLogger
config = dotenv_values(".env")

app = FastAPI()


sio = SocketManager(app=app)
path = Path.cwd()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.cache = None
conf = ConnectionConfig(
    MAIL_USERNAME = config["MAIL_USERNAME"],
    MAIL_PASSWORD = config["MAIL_PASSWORD"],
    MAIL_FROM = config["MAIL_FROM"],
    MAIL_PORT = config["MAIL_PORT"],
    MAIL_SERVER = config["MAIL_SERVER"],
    MAIL_FROM_NAME="Dave",
    MAIL_TLS = config["MAIL_TLS"],
    MAIL_SSL = config["MAIL_SSL"],
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False,
    MAIL_DEBUG=1,
    TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
)


#db = setupdb(config['REDISURL'],config['REDISPASS'],config['REDISDB'],config['REDISPORT'])
