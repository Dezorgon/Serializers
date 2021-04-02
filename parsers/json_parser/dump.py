import inspect
import types

_simple_type = (str, bool, int, float)


def obj_to_str(obj):
    return ''.join(obj_to_str_iter(obj))


def obj_to_str_iter(obj):
    if type(obj) in _simple_type or obj is None:
        yield simple_to_str(obj)
    elif isinstance(obj, (list, tuple)):
        yield from list_to_str(obj)
    elif isinstance(obj, dict):
        yield from dict_to_str(obj)
    elif inspect.isclass(obj):
        yield from class_to_str(obj)
    elif inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, types.LambdaType):
        yield from function_to_str(obj)
    elif hasattr(obj, '__dict__'):
        yield from object_to_str(obj)


def object_to_str(obj):
    yield f'object("{type(obj).__name__}"): '
    yield from complex_to_str(obj)


def class_to_str(obj):
    #yield f'class("{obj.__name__}"): '
    #bases = "".join(list_to_str(obj.__bases__))
    #if bases:
    #    yield f'class("{bases}"): '
    #yield from complex_to_str(obj)
    source = inspect.getsource(obj).replace('"', r'\"').replace("'", r'\'')
    yield f'class("{obj.__name__}"): "{source}"'


def function_to_str(obj):
    #source = re.sub(
    #    r"def \w+\(",
    #    "def func(",
    #    str(inspect.getsource(obj))
    #)
    source = inspect.getsource(obj).replace('"', '\"').replace("'", '\'')
    yield f'function("{obj.__name__}"): "{source}"'
    #source = '\n' + '\n'.join(str(inspect.getsource(obj)).split('\n')[1:])
    #yield 'function' + str(inspect.signature(obj)) + '{' + source + '}'


def complex_to_str(obj):
    yield "{"
    attr = dir(obj)
    for i, a in enumerate(attr):
        if not a.startswith('__'):
            yield f'"{a}"'
            yield ': '
            yield from obj_to_str(getattr(obj, a))
            if i < len(attr) - 1:
                yield ', '
    yield "}"


def simple_to_str(obj):
    obj_type = type(obj)
    if obj_type is str:
        return f'"{obj}"'
    elif obj is None:
        return 'null'
    elif obj_type is bool:
        return 'true' if obj else 'false'
    elif obj_type is int:
        return int.__repr__(obj)
    elif obj_type is float:
        if obj != obj:
            return 'NaN'
        elif obj == float('inf'):
            return 'Infinity'
        elif obj == -float('inf'):
            return '-Infinity'
        else:
            return float.__repr__(obj)
    else:
        return str(obj)


def list_to_str(obj):
    yield '['

    for i, val in enumerate(obj):
        yield from obj_to_str(val)

        if i < len(obj) - 1:
            yield ', '

    yield ']'


def dict_to_str(obj):
    yield '{'

    for i, (key, val) in enumerate(obj.items()):
        yield f'"{key}": '
        yield from obj_to_str(val)

        if i < len(obj) - 1:
            yield ', '

    yield '}'
