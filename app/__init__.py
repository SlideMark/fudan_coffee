from flask import Flask
from core.config import Config

app = Flask(__name__, template_folder='view')
conf = Config()

from app.controller.user import *
from app.controller.event import *
from app.controller.account import *
from app.controller.home import *
from app.controller.product import *
from app.controller.ledger import *
from app.controller.payment import *
from app.controller.cart import *