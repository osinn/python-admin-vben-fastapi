import re


def camel_to_snake(name: str) -> str:
    """
    驼峰转下划线
    :param name:
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(snake_str: str) -> str:
    """
    下划线转驼峰命名
    :param snake_str:
    :return:
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])
