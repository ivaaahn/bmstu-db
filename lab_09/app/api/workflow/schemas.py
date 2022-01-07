from marshmallow import Schema, fields, pre_load

from app.api.app.schemas import ResponseSchema


class OrderDetailsSchema(Schema):
    product_id = fields.Int()
    amount = fields.Int()


class OrderCreateRequestSchema(Schema):
    customer_id = fields.Int(required=True)
    restaurant_id = fields.Int(required=True)
    dst_address = fields.Int(required=True)
    src_address = fields.Int(required=True)
    products = fields.List(fields.Nested(OrderDetailsSchema))


class OrderCreateDataResponseSchema(Schema):
    order_id = fields.Int(required=True)
    order_number = fields.Int(required=True)
    employee_id = fields.Int(required=True)
    status = fields.Int(required=True)


class OrderCreateResponseSchema(ResponseSchema):
    data = fields.Nested(OrderCreateDataResponseSchema, many=False)


class OrderUpdateRequestSchema(Schema):
    id = fields.Int(required=True)
    dst_address = fields.Int(required=True)


class OrderUpdateResponseSchema(ResponseSchema):
    order_id = fields.Int(allow_none=True)


class OrderDeleteRequestSchema(Schema):
    id = fields.Int(required=True)


class OrderDeleteResponseSchema(ResponseSchema):
    order_id = fields.Int(required=False)
