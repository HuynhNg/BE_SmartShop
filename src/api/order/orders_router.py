from fastapi import APIRouter, Depends
from src.dto.order_dto import Order, OrderDetail, NewOrder, NewOrderDetail
from src.api.order.orders_controller import OrdersController
from src.middlewares.verify_middleware import admin_verify, user_verify
from fastapi_cache.decorator import cache 

router = APIRouter(prefix="/orders", tags=["Orders"])

orders_ctl = OrdersController()

@router.get("/", dependencies=[Depends(admin_verify)])
@cache(expire=300)
def get_all_orders(Page: int = 1):
    return orders_ctl.get_all_orders(Page)

@router.get("/{id}", dependencies=[Depends(admin_verify)])
def get_order_details(id: int):
    return orders_ctl.get_order_details(id)

@router.post("/", dependencies=[],)
def create_order(order: NewOrder, user=Depends(user_verify)):
    return orders_ctl.create_order(order, user)

@router.delete("/{id}", dependencies=[Depends(admin_verify)])
def delete_order(order_id: int):
    return orders_ctl.delete_order(order_id)
