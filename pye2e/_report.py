import re
import time
from ._project_config import config


def save_as_text(log):
    time_str = time.strftime("%Y%m%d-%H%M%S")
    log = _clean_test(log)
    path = config['report']['path'] + time_str + '.log'
    with open(path, 'w') as report:
        report.write(log)


def _clean_test(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)
