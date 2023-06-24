from marshmallow import Schema, fields, validate

class Register(Schema):
    first_name = fields.String(required=True, validate=validate.Length(max=50, min=1))
    last_name = fields.String(required=True, validate=validate.Length(max=50, min=1))
    email = fields.Email(required=True, validate=validate.Length(max=50, min=1))
    password = fields.String(required=True, validate=validate.Length(max=50, min=1))

register = Register()


