from marshmallow import Schema, fields


class ResponseSchema(Schema):
    status = fields.Int()
