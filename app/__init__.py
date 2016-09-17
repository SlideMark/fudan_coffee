from flask import Flask
from core.config import Config
import os

app = Flask(__name__, template_folder='view')
conf = Config()
app.debug = conf.debug

modules = os.listdir(os.getcwd()+'/app/controller/')
pymodule = [each for each in modules if each.endswith('.py')]
for each in modules:
    exec('from app.controller.{} import *'.format(each.split('.')[0]))
