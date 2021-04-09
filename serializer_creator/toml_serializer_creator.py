from serializer_creator.abstract_serializer_creator import AbstractSerializerCreator
from parsers.toml_parser.parser import TomlParser
from serializer_creator.parser_interface import Parser


class TomlSerializerCreator(AbstractSerializerCreator):
    def create_serializer(self) -> Parser:
        return TomlParser()
