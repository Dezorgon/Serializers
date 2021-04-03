from parsers.json_parser.dump import obj_to_str
from parsers.json_parser.load import str_to_obj
from serializer_creator.parser_interface import Parser


class JsonParser(Parser):
    def dump(self, obj, fp):
        fp.write(obj_to_str(obj))

    def dumps(self, obj) -> str:
        return obj_to_str(obj)

    def load(self, fp):
        doc = fp.read()
        if doc == '':
            return ''
        return str_to_obj(doc)

    def loads(self, s):
        if s == '':
            return ''
        return str_to_obj(s)

def f():
    print(1)


print(JsonParser().dumps(f))