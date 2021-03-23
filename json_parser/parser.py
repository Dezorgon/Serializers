from json_parser.dump import obj_to_str
from json_parser.load import str_to_obj
from serializer_creator.parser_interface import Parser


class JsonParser(Parser):
    def dump(self, obj, fp):
        fp.write(obj_to_str(obj))

    def dumps(self, obj) -> str:
        return obj_to_str(obj)

    def load(self, fp):
        doc = fp.read()
        return str_to_obj(doc)

    def loads(self, s):
        return str_to_obj(s)


class abc(object):
    a = None
    b = [1, (1, 5)]
    c = False
    d = "gds"
    e = {"a": 11, "b": {1: 21, 2: 22}}

    def f(self, s, k):
        v = 1 + 2 + s - k
        return v

    class gg():
        a = None
        b = [1, (1, 5)]
        c = False
        d = 'gds'

    m = gg()

n = abc()


def func(l):
    l += 55
    return l


#print(''.join(obj_to_str(n)))

with open('../text.txt', 'w') as fp:
    dump(abc, fp)

with open('../text.txt', 'r') as fp:
    k = load(fp)
    print(k.f(5, 4))

