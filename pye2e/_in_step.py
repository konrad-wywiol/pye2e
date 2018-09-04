import re


def find_params(step):
    return re.findall(r'"(.*?)"', step)


def find_text_without_params(step):
    parameters = find_params(step)
    for parameter in parameters:
        parameter = ' "' + parameter + '"'
        step = step.replace(parameter, '')
    return step
