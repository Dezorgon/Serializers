from serializer_creator.abstract_serializer_creator import AbstractSerializerCreator
from parsers.yaml_parser.parser import YamlParser
from serializer_creator.parser_interface import Parser


class YamlSerializerCreator(AbstractSerializerCreator):
    def create_serializer(self) -> Parser:
        return YamlParser()
