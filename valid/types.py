import json

from .error import FieldNotFound, UnableCastDataToTemplate
import re


class BaseType:
    @staticmethod
    def name():
        return 'none'

    def norm(self, data, key):
        return data


class IntType(BaseType):
    @staticmethod
    def name():
        return 'int'

    def norm(self, data, key):
        try:
            return int(data)
        except (TypeError, ValueError):
            raise UnableCastDataToTemplate(template={key: self.name()}, data={key: data})


class FloatType(BaseType):
    @staticmethod
    def name():
        return 'float'

    def norm(self, data, key):
        try:
            return float(data)
        except (TypeError, ValueError):
            raise UnableCastDataToTemplate(template={key: self.name()}, data={key: data})


class StrType(BaseType):
    @staticmethod
    def name():
        return 'str'

    def norm(self, data, key):
        try:
            return str(data)
        except (TypeError, ValueError):
            raise UnableCastDataToTemplate(template={key: self.name()}, data={key: data})


class PhoneType(BaseType):
    def __init__(self):
        self.number_re = re.compile(r'\d+')
        self.phone_re = re.compile(r'9\d{9}')

    @staticmethod
    def name():
        return 'phone'

    def norm(self, data, key):
        try:
            phone = self.phone_re.findall(''.join(self.number_re.findall(data)))
            if type(phone) == list and len(phone) == 1 and len(phone[0]) == 10:
                return '7' + phone[0]
            else:
                raise TypeError
        except (TypeError, ValueError):
            raise UnableCastDataToTemplate(template={key: self.name()}, data={key: data})


class ArrayType(BaseType):
    def __init__(self, item_class_type: BaseType):
        self.array_re = re.compile(r'^\[(.*)\]$')
        self.item_class_type = item_class_type

    def name(self):
        return 'array<' + self.item_class_type.name() + '>'

    def norm(self, data, key):
        try:
            if type(data) == str:
                data = self.array_re.match(data)
                if data is None:
                    raise UnableCastDataToTemplate(template={key: self.name()}, data={key: data})
                data = list(map(lambda x: x.strip(), data.group(1).split(',')))

            return_data = []
            for i, item in enumerate(data):
                return_data.append(self.item_class_type.norm(data=item, key=i))
        except (TypeError, ValueError):
            raise UnableCastDataToTemplate(template={key: self.name()}, data={key: data})

        return return_data


class StructureType:
    def __init__(self, template: dict):
        self.template = template
        self.str_type = StrType()

    @staticmethod
    def name():
        return 'struct'

    def norm(self, data, key):
        result = dict()

        for class_key, class_type in self.template.items():
            if class_key not in data:
                raise FieldNotFound(data={class_key: None}, template={class_key: class_type.name()})
            if class_type is None:
                class_type = self.str_type

            try:
                result[class_key] = class_type.norm(data=data[class_key], key=class_key)
            except (FieldNotFound, UnableCastDataToTemplate):
                raise UnableCastDataToTemplate(data={key: data}, template={key: self.name()},
                                               struct_template=self.template)
        return result
