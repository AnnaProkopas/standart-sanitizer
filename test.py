from valid.validator import normalize, Types, BaseType
from valid.error import FieldNotFound, UnableCastDataToTemplate
import unittest


class BaseInput:
    def __init__(self, data: str, class_type: BaseType, result) -> None:
        self.data = '{"foo": ' + data + '}'
        self.template = {'foo': class_type}
        self.invalid_template = {'boo': class_type}
        self.result = {'foo': result}


class BaseTest:
    input_type = None

    def test_valid(self):
        self.assertDictEqual(normalize(self.input_type.data, self.input_type.template), self.input_type.result)

    def test_invalid_int_template(self):
        self.assertRaises(FieldNotFound, normalize, self.input_type.data, self.input_type.invalid_template)


def test_invalid(invalid_data_class):
    try:
        normalize(invalid_data_class.data, invalid_data_class.template)
    except UnableCastDataToTemplate:
        assert True
    except Exception as e:
        assert False
    else:
        assert False


intInput = BaseInput('"123"', Types.int(), 123)
floatInput = BaseInput('"12.2"', Types.float(), 12.2)
strInput = BaseInput('"bar"', Types.str(), 'bar')
phoneInput = BaseInput('"+7(902)44-55-222"', Types.phone(), '79024455222')

arrayIntInput = BaseInput('["0", "1", "2", "3"]', Types.array(Types.int()), [0, 1, 2, 3])
arrayFloatInput = BaseInput('["0.02", "10.1", "2.1", "3.5"]', Types.array(Types.float()), [0.02, 10.1, 2.1, 3.5])
arrayStrInput = BaseInput('["a", "b", "c", "..."]', Types.array(Types.str()), ['a', 'b', 'c', '...'])
arrayPhoneInput = BaseInput('["89244444442", "8(924)4444442", "+7(924)44-444-42", "+7(924) 44-444-42"]',
                            Types.array(Types.phone()), ['79244444442', '79244444442', '79244444442', '79244444442'])
arrayPhoneInput1 = BaseInput('["89244444442", "8", "+7(924)44-444-42", "+7(924) 44-444-42"]',
                             Types.array(Types.float()), ['79244444442', '79244444442', '79244444442', '79244444442'])

struct = {
    'int': Types.int(),
    'float': Types.float(),
    'str': Types.str(),
    'phone': Types.phone(),
    'description': Types.str(),
    'array': Types.array(Types.float()),
}
post_struct_data = """
{
    "int": "10", "float": "10.05", "str": "string", "phone": "+7 999 55 44 11 1", 
    "description": ["2021-01-01 12:00:05", "2021.03.05 5pm"],
    "array": ["0.05", "0.01", "1.2", "11.0"]
    }
"""
result_struct_data = {
    "int": 10, "float": 10.05, "str": "string", "phone": "79995544111",
    "description": "['2021-01-01 12:00:05', '2021.03.05 5pm']",
    "array": [0.05, 0.01, 1.2, 11.0]
}
structInput = BaseInput(post_struct_data, Types.struct(struct), result_struct_data)


class TestInt(BaseTest, unittest.TestCase):
    input_type = intInput


class TestFloat(BaseTest, unittest.TestCase):
    input_type = floatInput


class TestStr(BaseTest, unittest.TestCase):
    input_type = strInput


class TestPhone(BaseTest, unittest.TestCase):
    input_type = phoneInput

    def test_valid_another_format(self):
        self.assertDictEqual(normalize('{"foo": "8902-445-52-22"}', self.input_type.template), self.input_type.result)
        self.assertDictEqual(normalize('{"foo": "8 (902) 445 52 22"}', self.input_type.template),
                             self.input_type.result)

    def test_invalid_type_template(self):
        city_phone = BaseInput('"2 44 55 22"', Types.phone(), '74232445522')
        test_invalid(city_phone)


class TestArrayInt(BaseTest, unittest.TestCase):
    input_type = arrayIntInput


class TestArrayFloat(BaseTest, unittest.TestCase):
    input_type = arrayFloatInput


class TestArrayStr(BaseTest, unittest.TestCase):
    input_type = arrayStrInput


class TestArrayPhone(BaseTest, unittest.TestCase):
    input_type = arrayPhoneInput


class TestMultiJson(unittest.TestCase):
    def test_valid(self):
        data = '{"foo": "123", "bar": "asd", "baz": "8 (950) 288-56-23"}'
        template = {'foo': Types.int(), 'bar': Types.str(), 'baz': Types.phone()}
        result = {'foo': 123, 'bar': 'asd', 'baz': '79502885623'}
        self.assertDictEqual(normalize(data, template), result)


class TestStruct(BaseTest, unittest.TestCase):
    input_type = structInput


if __name__ == '__main__':
    unittest.main()
