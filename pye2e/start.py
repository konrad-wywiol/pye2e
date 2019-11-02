import sys
from ._load_config import load_config_and_run_pye2e as start


sys.modules[__name__] = start
