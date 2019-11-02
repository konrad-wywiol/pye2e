import os
import tempfile


config = None


def change_config(config_module):
    global config
    wip_config = config_module.config
    wip_config_path = os.path.dirname(config_module.__file__)
    config = _fix_paths(wip_config, wip_config_path)


def _fix_paths(cfg, cfg_path):
    if cfg['directory_path']['default_path']:
        cfg['directory_path']['paths']['features'] = cfg_path + '/features/'
        cfg['directory_path']['paths']['steps'] =  cfg_path + '/steps/'
    else:
        for key, value in cfg['directory_path']['paths'].items():
            cfg['directory_path'][key] = _add_slash_at_the_end(value)
    return cfg


def _add_slash_at_the_end(string):
    if string[-1:] != '/':
        return string + '/'

    return string
