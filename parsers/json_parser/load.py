import copy
import inspect
import types
from codecs import encode

from parsers.json_parser.tokens import *


def str_to_obj(doc):
    tokens = doc_to_tokens(doc)
    obj = tokens_to_obj(tokens)
    bind_methods(obj)
    return obj


def bind_methods(obj):
    funcs = dict(inspect.getmembers(obj, inspect.isfunction))

    for name in funcs:
        args = list(inspect.signature(funcs[name]).parameters)
        funcs[name].__name__ = name
        if len(args) > 0 and args[0] == 'self':
            bound_method = funcs[name].__get__(obj, obj.__class__)
            setattr(obj, name, bound_method)

    for name, val in inspect.getmembers(obj):
        if inspect.isclass(val) and not name.startswith('__'):
            bind_methods(val)


def tokens_to_obj(tokens):
    parsers = (parse_function, parse_class, parse_object, parse_dict, parse_array)

    d = dict(zip(flags + ('{', '['), parsers))

    if tokens[0] in d:
        return d[tokens.pop(0)](tokens)

    return tokens.pop(0)


def dict_to_obj(d, name):
    if not isinstance(d, dict):
        return d

    obj = type(name, (), {})
    obj = obj()

    for key in d:
        obj.__dict__[key] = d[key]

    return obj


def parse_object(tokens):
    name = tokens.pop(0)
    tokens.pop(0)
    obj_dict = parse_dict(tokens)
    return dict_to_obj(obj_dict, name)


def parse_class(tokens):
    # tokens.pop(0)
    # if tokens[0] == 'class':
    #    tokens.pop(0)
    #    bases = tokens.pop(0)
    # obj_dict = parse_dict(tokens)
    # return type(name, (), obj_dict)
    name = tokens.pop(0)
    d = {}
    source = tokens[0].strip()
    tokens.pop(0)
    exec(source, d)
    return d[name]


def _make_cell():
    if False:
        cell = None
    return (lambda: cell).__closure__[0]


def parse_function(tokens):
    def f():
        pass

    name = tokens.pop(0)
    tokens.pop(0)
    d = parse_dict(tokens)

    co: types.CodeType = compile(d['source'].strip(), '<string>', 'exec')
    co = co.co_consts[0]
    co_freevars = tuple(d['closure'].keys())
    co_names = tuple([e for e in co.co_names if e not in d['closure']])
    co_code = d['byte_code']
    co_code = encode(co_code, "raw_unicode_escape")
    co = co.replace(co_freevars=co_freevars, co_name=name, co_names=co_names, co_code=co_code)

    gl = dict(**d['globals'], **{'__builtins__': __builtins__})

    closure = []
    for k in d['closure']:
        cell = _make_cell()
        cell.cell_contents = d['closure'][k]
        closure.append(cell)

    func = types.FunctionType(code=co, globals=gl, closure=tuple(closure))
    return func


def parse_function2(tokens):
    def f():
        pass

    name = tokens.pop(0)
    tokens.pop(0)
    d = parse_dict(tokens)

    co_freevars = tuple(d['closure'].keys())
    co_names = tuple(d['names'])
    co_code = d['byte_code']
    co_code = encode(co_code, "raw_unicode_escape")
    co = f.__code__
    co = co.replace(co_freevars=co_freevars, co_name=name, co_names=co_names, co_code=co_code)

    gl = dict(**d['globals'], **{'__builtins__': __builtins__})

    closure = []
    for k in d['closure']:
        cell = _make_cell()
        cell.cell_contents = d['closure'][k]
        closure.append(cell)

    func = types.FunctionType(code=co, globals=gl, closure=tuple(closure))
    return func


def parse_dict(tokens):
    _object = {}

    if tokens[0] == '}':
        tokens.pop(0)
        return _object

    while True:
        key = tokens.pop(0)

        if tokens.pop(0) != ':':
            raise Exception()

        val = tokens_to_obj(tokens)
        _object[key] = val

        token = tokens.pop(0)
        if token == '}':
            return _object
        if token != ',':
            raise Exception()


def parse_array(tokens):
    _array = []

    if tokens[0] == ']':
        tokens.pop(0)
        return _array

    while True:
        val = tokens_to_obj(tokens)
        _array.append(val)

        token = tokens.pop(0)
        if token == ']':
            return _array
        if token != ',':
            raise Exception()
