import dis
import inspect
import opcode
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


GLOBAL_OPS = (opcode.opmap['STORE_GLOBAL'], opcode.opmap['DELETE_GLOBAL'], opcode.opmap['LOAD_GLOBAL'])

def _walk_global_ops(code):
    for instr in dis.get_instructions(code):
        op = instr.opcode
        if op in GLOBAL_OPS:
            yield op, instr.arg


def function_to_str(func):
    source = inspect.getsource(func).replace('"', '\"').replace("'", '\'')
    co = func.__code__
    names = co.co_names
    _globals = {names[oparg] for _, oparg in _walk_global_ops(co)}
    _globals = {k: func.__globals__[k] for k in _globals if k in func.__globals__}
    _closure = dict()
    if func.__closure__ is not None:
        _closure = dict((co.co_freevars[i], c.cell_contents) for i, c in enumerate(func.__closure__))

    _names = tuple([e for e in co.co_names if e not in _closure.keys()])
    _globals = obj_to_str(_globals).strip('"')
    _closure = obj_to_str(_closure).strip('"')
    _code = obj_to_str(str(co.co_code)[2:-1].encode().decode('unicode_escape'))

    yield f'function("{func.__name__}"): ' \
          f'{{"source": "{source}", "globals": {_globals}, "closure": {_closure}, "byte_code": {_code}}}'


def function_to_str2(func): # pragma: no cover
    source = inspect.getsource(func).replace('"', '\"').replace("'", '\'')
    co = func.__code__
    names = co.co_names
    _globals = {names[oparg] for _, oparg in _walk_global_ops(co)}
    _globals = {k: func.__globals__[k] for k in _globals if k in func.__globals__}
    _closure = dict()
    if func.__closure__ is not None:
        _closure = dict((co.co_freevars[i], c.cell_contents) for i, c in enumerate(func.__closure__))

    _names = obj_to_str([e for e in co.co_names if e not in _closure.keys()])
    _globals = obj_to_str(_globals).strip('"')
    _closure = obj_to_str(_closure).strip('"')
    _code = obj_to_str(str(co.co_code)[2:-1].encode().decode('unicode_escape'))

    yield f'function("{func.__name__}"): ' \
          f'{{"source": "{source}", "names": {_names}, "globals": {_globals}, "closure": {_closure}, "byte_code": {_code}}}'


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





# function_to_str(1)
# print(1)
# func = f
# source = inspect.getsource(func).replace('"', '\"').replace("'", '\'')
# co = compile(source, '<string>', 'exec')
# co = co.co_consts[0]
# names = co.co_names
# _globals = {names[oparg] for _, oparg in _walk_global_ops(co)}
# _globals = {k: obj_to_str(func.__globals__[k]) for k in _globals if k in func.__globals__}
# gl = dict(**_globals, **{'__builtins__': __builtins__})
# _globals = obj_to_str(_globals)
# fff = types.FunctionType(co, gl)
# fff()
# print(f'function("{func.__name__}"): {{"source": "{source}", "globals": {_globals}}}')
