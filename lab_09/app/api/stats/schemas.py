from marshmallow import Schema, fields

from app.api.app.schemas import ResponseSchema


class StatsRequestSchema(Schema):
    cached = fields.Bool(required=False, missing=False)


class StatsItemResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    summary = fields.Int()
    number_of_orders = fields.Int()


class StatsListResponseSchema(ResponseSchema):
    data = fields.Nested(StatsItemResponseSchema, many=True)
