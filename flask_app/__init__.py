from flask import Flask, Blueprint
import logging
import time
import sys
import json

# Enable logging
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.INFO)
# logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.getLogger("chardet.charsetprober").disabled = True

app = Flask(__name__)
app.config.from_pyfile('config.py')
logger.info("app root_path:" + app.root_path)

api_bp = Blueprint("Sample", __name__)
from flask_app import wire

app.register_blueprint(api_bp, url_prefix="/api")

print(app.url_map)


