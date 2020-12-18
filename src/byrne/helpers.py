from dataclasses import field


def default(factory):
    return field(default_factory=factory)


def set_optional_arg(name, val, args):
    if val is not None:
        args[name] = val


def first_kvp(dct: dict):
    return next(iter(dct.items()))


def invert_dict(dct: dict):
    return {v: k for k, v in dct.items()}


def autoclassifier(datatype):
    return lambda x: isinstance(x, datatype)
