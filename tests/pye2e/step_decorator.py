from . import _in_step


def step(step_param):
    def _step(func):
        def decorated_func(*args, **kwargs):
            func(*args, **kwargs)
            return func
        decorated_func.decorator = step
        decorated_func.__name__ = func.__name__
        decorated_func.step_text_without_params = _in_step.find_text_without_params(step_param)
        return decorated_func

    return _step
