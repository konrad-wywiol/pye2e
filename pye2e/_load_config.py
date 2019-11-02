def load_config_and_run_pye2e(config_module):
    from . import _project_config
    _project_config.change_config(config_module)

    from . import _main
    _main.start()
