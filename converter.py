from enum import Enum
from serializer_creator.json_serializer_creator import JsonSerializerCreator


class ParsersEnum(Enum):
    JSON = JsonSerializerCreator


def convert(deserializer, serializer, file_to_convert, file_to_save):
    if not isinstance(deserializer, ParsersEnum):
        raise TypeError('serializer must be an instance of ParsersEnum')
    if not isinstance(serializer, ParsersEnum):
        raise TypeError('deserializer must be an instance of ParsersEnum')

    serializer_creator = deserializer.value()
    serializer_obj = serializer_creator.create_serializer()
    obj = serializer_obj.load(file_to_convert)
    file_to_convert.close()

    deserializer_creator = serializer.value()
    deserializer_obj = deserializer_creator.create_serializer()
    deserializer_obj.dump(obj, file_to_save)
    file_to_save.close()


#convert(ParsersEnum.JSON, ParsersEnum.JSON, open('text.txt', 'r'), open('text2.txt', 'w'))
