project_config = {
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
    }
}


def change_config(config):
    global project_config
    config = _fix_paths(config)
    project_config = config


def _fix_paths(config):
    for key, value in config['directory_path'].items():
        config['directory_path'][key] = _add_slash_at_the_end(value)

    return config


def _add_slash_at_the_end(string):
    if string[-1:] != '/':
        return string + '/'

    return string
