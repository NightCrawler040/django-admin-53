# logger.py
from pathlib import Path
import logging

# Создание пользовательский журнал
logger = logging.getLogger(__name__)
logger.propagate = False
logging.basicConfig(level=logging.DEBUG)

# Создание обработчики
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('my_log_file.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Создание форматтеры и добавление их к обработчикам
c_format = logging.Formatter('myapp: %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Добавление обработчики в журнал
logger.addHandler(c_handler)
logger.addHandler(f_handler)


def log(frame, obj):
    """Создание сообщение журнала и обратный объект."""
    path = Path(frame)
    module = path.stem
    line = frame
    message_text = f'{obj} <{module}> {line}'
    logger.warning(message_text)
    return obj
