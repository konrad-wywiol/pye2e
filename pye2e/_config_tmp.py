config = {
    'directory_path': {
        'features': '',
        'steps': ''
    },
    'debug': False,
    'timeout': 0,
    'browser': '',
    'selenium_host': '',
    'fullscreen': False,
    'main_url': '',
    'custom_wait': {
        'active': False,
        'loading_object_XP': [],
        'custom_timeout': 0
    },
    'report': {
        'active': False,
        'path': ''
    }
}


def change_config(cfg):
    global config
    cfg = _fix_paths(cfg)
    config = cfg


def _fix_paths(cfg):
    for key, value in cfg['directory_path'].items():
        cfg['directory_path'][key] = _add_slash_at_the_end(value)

    return cfg


def _add_slash_at_the_end(string):
    if string[-1:] != '/':
        return string + '/'

    return string
