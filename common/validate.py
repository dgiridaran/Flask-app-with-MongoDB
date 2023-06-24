from flask import request
def validator(schema):
    def validate(func):
        def wrapper_func(*args, **kwargs):
            data = request.get_json()
            try:
                schema.load(data)
            except Exception as e:
                return {"Error":str(e)}, 400
            return func(*args, **kwargs)
        return wrapper_func
    return validate
    