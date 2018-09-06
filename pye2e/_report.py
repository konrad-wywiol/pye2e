import re
import time
from . import _config_tmp


def save_as_text(log):
    time_str = time.strftime("%Y%m%d-%H%M%S")
    log = _clean_test(log)
    path = _config_tmp.config['report']['path'] + time_str + '.log'
    with open(path, 'w') as report:
        report.write(log)


def _clean_test(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)
