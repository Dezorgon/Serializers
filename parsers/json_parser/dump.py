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


STORE_GLOBAL = opcode.opmap['STORE_GLOBAL']
DELETE_GLOBAL = opcode.opmap['DELETE_GLOBAL']
LOAD_GLOBAL = opcode.opmap['LOAD_GLOBAL']
GLOBAL_OPS = (STORE_GLOBAL, DELETE_GLOBAL, LOAD_GLOBAL)

def _walk_global_ops(code):
    for instr in dis.get_instructions(code):
        op = instr.opcode
        if op in GLOBAL_OPS:
            yield op, instr.arg

def f():
     print(123)

def function_to_str(func):
    func = f
    source = inspect.getsource(func).replace('"', '\"').replace("'", '\'')
    co = compile(source, '<string>', 'exec')
    #d = {}
    #exec(co, d)
    #d['f']()
    print(co.co_consts[0].co_code)
    #co = func.__code__
    co = co.co_consts[0]
    names = co.co_names
    f_globals_ref = {names[oparg] for _, oparg in _walk_global_ops(co)}
    f_globals = {k: obj_to_str(func.__globals__[k]) for k in f_globals_ref if k in func.__globals__}
    gl = dict(**f_globals, **{'__builtins__': __builtins__})
    f_globals = obj_to_str(f_globals)
    fff = types.FunctionType(co, gl)
    fff()
    #source = inspect.getsource(obj).replace('"', '\"').replace("'", '\'')
    yield f'function("{func.__name__}"): {source} {f_globals}'


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
