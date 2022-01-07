from dataclasses import dataclass


@dataclass
class OrderDetails:
    product_id: int
    amount: int


@dataclass
class CreateOrder:
    customer_id: int
    employee_id: int
    restaurant_id: int
    dst_address: int
    src_address: int
    order_number: int
    status: int
    products: list[OrderDetails]


@dataclass
class UpdateOrder:
    id: int
    dst_address: int


@dataclass
class DeleteOrder:
    id: int
