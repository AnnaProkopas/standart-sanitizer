import json
from valid.types import *
from .error import FieldNotFound


def normalize(json_string: str, template: dict):
    json_data = json.loads(json_string)

    result = dict()
    for key, class_type in template.items():
        if key not in json_data:
            raise FieldNotFound(object={key: None})
        try:
            result[key] = class_type.norm(data=json_data[key], key=key)
        except UnableCastDataToTemplate as error:
            raise error
        except Exception as e:
            message = str(e) + (': {"%s": "%s"}' % (key, json_data[key]))
            raise type(e)(message)

    return result


class Types:
    none = BaseType
    int = IntType
    float = FloatType
    str = StrType
    phone = PhoneType
    array = ArrayType
    struct = StructureType
