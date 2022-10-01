import logging
from flask import Flask

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(usuarioID)s - %(ip)s - %(token)s')

file_handler = logging.FileHandler('logAlarmas.txt')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

alarmasLog = Flask(__name__)

@alarmasLog.route("/")
def loggerAlarma(alarmaProcesada):
    return logger.info('',extra=alarmaProcesada)


