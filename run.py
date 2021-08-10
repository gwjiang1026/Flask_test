# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""
import os
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)-5s [%(filename)-8s](%(lineno)s): %(message)s',
            'datefmt': '%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'stdout': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'rollingFile': {
            'formatter': 'standard',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': './logs/trade{}.log'.format(os.getenv('sample', '')),  # TimedRotatingFileHandler
            "when": "midnight",
            "encoding": "utf-8"
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['stdout', 'rollingFile'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

from flask_app import app

#----------------------------------------
# launch
#----------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False)
