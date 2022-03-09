from logging.config import dictConfig
import logging
import logging.handlers
from multiprocessing import Queue

from config import get_settings, get_log_config

dictConfig(get_log_config().dict())
logger = logging.getLogger("csvfastapi")
# logging_queue = Queue(-1)
# queue_handler = logging.handlers.QueueHandler(logging_queue)
# queue_handler.setLevel(logging.ERROR)
#
# logger.addHandler(queue_handler)
settings = get_settings()
smtp_handler = logging.handlers.SMTPHandler(mailhost=(settings.mail_server, settings.mail_port),
                                            fromaddr=settings.mail_from,
                                            toaddrs=[settings.mail_from],
                                            subject='Critical error API',
                                            credentials=(settings.mail_username, settings.mail_password),
                                            secure=())
#
smtp_handler.setLevel(logging.ERROR)
# smtp_formatter = logging.Formatter("%(levelprefix)s | %(asctime)s | [%(filename)s:%(lineno)d] | %(message)s")
# smtp_handler.setFormatter(smtp_formatter)
# queue_listener = logging.handlers.QueueListener(logging_queue, smtp_handler)
# queue_listener.start()
file_handler = logging.handlers.RotatingFileHandler('api.log', maxBytes=10485760, backupCount=300, encoding='utf-8')

logger.addHandler(smtp_handler)
logger.addHandler(file_handler)

