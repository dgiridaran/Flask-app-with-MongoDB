from marshmallow import Schema, fields

class Login(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

login = Login()