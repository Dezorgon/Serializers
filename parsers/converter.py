import inspect
import types

_simple_type = (str, bool, int, float)
function_flag = '_func'
class_flag = '_class'
object_flag = '_object'


def serialize(obj):
    if type(obj) in _simple_type:
        return obj
    elif type(obj) is dict:
        for k in obj:
            obj[k] = serialize(obj[k])
        return obj
    elif isinstance(obj, list) or isinstance(obj, tuple):
        l = []
        for o in obj:
            l.append(serialize(o))
        return l
    elif inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, types.LambdaType):
        return {function_flag: {obj.__name__: inspect.getsource(obj).strip()}}
    elif inspect.isclass(obj):
        return {class_flag: {obj.__name__: inspect.getsource(obj).strip()}}
    elif hasattr(obj, '__dict__'):
        tmp = {}
        d = {object_flag: {type(obj).__name__: tmp}}
        for a in dir(obj):
            if a.startswith('__'):
                continue
            val = getattr(obj, a)
            if type(val) in _simple_type:
                tmp[a] = val
            else:
                tmp[a] = serialize(val)
        return d


def deserialize(obj):
    if type(obj) in _simple_type:
        return obj
    elif isinstance(obj, list) or isinstance(obj, tuple):
        l = []
        for o in obj:
            l.append(deserialize(o))
        return l
    elif isinstance(obj, dict):
        for key, val in obj.items():
            if key == class_flag or key == function_flag:
                _d = {}
                items = val.items()
                name, source = list(items)[0]
                exec(source, _d)
                return _d[name]
            elif key == object_flag:
                items = val.items()
                name, d = list(items)[0]
                o = type(name, (), {})
                o = o()
                for k in d:
                    o.__dict__[k] = deserialize(d[k])
                return o
            elif type(val) in _simple_type:
                pass
            elif isinstance(val, list) or isinstance(val, tuple):
                l = []
                for o in val:
                    l.append(deserialize(o))
                obj[key] = l
            return obj
