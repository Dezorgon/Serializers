from enum import Enum
from serializer_creator.json_serializer_creator import JsonSerializerCreator
from serializer_creator.yaml_serializer_creator import YamlSerializerCreator
from serializer_creator.toml_serializer_creator import TomlSerializerCreator
from serializer_creator.pickle_serializer_creator import PickleSerializerCreator


class ParsersEnum(Enum):
    JSON = JsonSerializerCreator
    YAML = YamlSerializerCreator
    TOML = TomlSerializerCreator
    PICKLE = PickleSerializerCreator


def convert(deserializer, serializer, file_to_convert, file_to_save=None):
    if not isinstance(deserializer, ParsersEnum):
        raise TypeError('serializer must be an instance of ParsersEnum')
    if not isinstance(serializer, ParsersEnum):
        raise TypeError('deserializer must be an instance of ParsersEnum')

    if deserializer == serializer:
        return

    if deserializer == ParsersEnum.PICKLE:
        file_to_convert = open(file_to_convert, 'rb')
    else:
        file_to_convert = open(file_to_convert, 'r')
    if file_to_save is not None:
        if serializer == ParsersEnum.PICKLE:
            file_to_save = open(file_to_save, 'w')
        else:
            file_to_save = open(file_to_save, 'wb')

    deserializer_creator = deserializer.value()
    deserializer_obj = deserializer_creator.create_serializer()
    obj = deserializer_obj.load(file_to_convert)
    file_name = file_to_convert.name
    file_to_convert.close()

    serializer_creator = serializer.value()
    serializer_obj = serializer_creator.create_serializer()
    if file_to_save is None:
        if serializer == ParsersEnum.PICKLE:
            file_to_save = open(file_name, 'wb')
        else:
            file_to_save = open(file_name, 'w')
    serializer_obj.dump(obj, file_to_save)
    file_to_save.close()

