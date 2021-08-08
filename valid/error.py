import json


class CastBaseException(Exception):
    text = ''

    def __init__(self, **kwargs):
        message = self.text
        if 'message' in kwargs:
            message = kwargs['message']

        if 'template' in kwargs and 'data' in kwargs:
            template = kwargs['template']
            data = kwargs['data']
            message += ', шаблон: ' + json.dumps(template) + ', данные: ' + json.dumps(data)
        if 'struct_template' in kwargs:
            struct = {}
            for key, item in kwargs['struct_template'].items():
                struct[key] = item.name()
            message += ', шаблон структуры: ' + json.dumps(struct)

        super().__init__(message)


class UnableCastDataToTemplate(CastBaseException):
    text = 'не удалось привести данные к типу '

    def __init__(self, **kwargs):
        message = self.text + list(kwargs['template'].values()).pop()
        kwargs['message'] = message
        super().__init__(**kwargs)


class FieldNotFound(CastBaseException):
    text = 'поле из шаблона не найдено'
