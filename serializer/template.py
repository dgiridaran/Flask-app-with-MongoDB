from marshmallow import Schema, fields

class Template(Schema):
    template_name = fields.String(required=True)
    subject = fields.String(required=True)
    body = fields.String(required=True)

template = Template()