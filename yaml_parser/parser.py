import yaml
from serializer_creator.parser_interface import Parser


import inspect
import types

_simple_type = (str, bool, int, float)


def obj_to_dict(obj):
    d = {}
    if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, types.LambdaType):
        return {'_func': inspect.getsource(obj).strip()}
    elif inspect.isclass(obj):
        return {'_class': inspect.getsource(obj).strip()}
    elif hasattr(obj, '__dict__'):
        tmp = {}
        d = {'_object': tmp}
        for a in dir(obj):
            if a.startswith('__'):
                continue
            val = getattr(obj, a)
            if type(val) in _simple_type:
                tmp[a] = val
            else:
                tmp[a] = obj_to_dict(val)
    return d


class YamlParser(Parser):
    def dump(self, obj, fp):
        yaml.dump(obj_to_dict(obj), fp)

    def dumps(self, obj) -> str:
        return yaml.dump(obj_to_dict(obj))

    def load(self, fp):
        doc = fp.read()
        if doc == '':
            return ''
        return str_to_obj(doc)

    def loads(self, s):
        if s == '':
            return ''
        return str_to_obj(s)