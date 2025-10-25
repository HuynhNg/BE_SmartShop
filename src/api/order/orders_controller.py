from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.api.order.orders_service import OrdersService
from src.dto.order_dto import NewOrder
from src.dto.product_dto import ProductOrder
from src.model.users_model import Users_model
from src.model.inventories_model import Inventories_model
from src.model.products_model import Products_model


class OrdersController:
    def get_all_orders(self, Page: int = 1):
        try:
            orders_sv = OrdersService()
            orders = orders_sv.get_all_orders(Page)
            return JSONResponse(
                content=jsonable_encoder({
                    "message": "Orders retrieved successfully",
                    "length": len(orders),
                    "orders": [order.dict() for order in orders],
                }),
                status_code=200,
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_order_details(self, OrderID: int):
        try:
            orders_sv = OrdersService()
            details = orders_sv.get_order_details(OrderID)
            return JSONResponse(
                content={
                    "message": "Order details retrieved successfully",
                    "length": len(details),
                    "details": [detail.dict() for detail in details],
                },
                status_code=200,
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def create_order(self, newOrder: NewOrder, payload_user: dict):
        try:
            user_id = payload_user.get("UserID") or payload_user.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid user token")

            user = Users_model.get_user_byID(user_id)
            if not user:
                return JSONResponse(content={"message": "UserID does not exist"}, status_code=404)

            # Điền thông tin mặc định nếu thiếu
            newOrder.UserName = newOrder.UserName or user.UserName
            newOrder.Address = newOrder.Address or user.Address
            newOrder.PhoneNumber = newOrder.PhoneNumber or user.PhoneNumber
            newOrder.Email = newOrder.Email or user.Email

            # Gom danh sách sản phẩm
            list_product = []
            if not len(newOrder.Orderdetail):
                return JSONResponse(
                        content={"message": f"Product does not exist"},
                        status_code=404,
                    )
            for item in newOrder.Orderdetail:
                inventory = Inventories_model.get_inventory_byProductID(item.ProductID)
                if not inventory:
                    return JSONResponse(
                        content={"message": f"ProductID {item.ProductID} does not exist"},
                        status_code=404,
                    )

                if int(inventory.Quantity) < int(item.Quantity):
                    return JSONResponse(
                        content={"message": f"ProductID {item.ProductID} not enough"},
                        status_code=400,
                    )

                product = Products_model.get_product_byID(item.ProductID)
                if not product.isActive:
                    return JSONResponse(
                        content={"message": f"ProductID {item.ProductID} is not available"},
                        status_code=400,
                    )

                list_product.append(
                    ProductOrder(
                        ProductID=product.ProductID,
                        ProductName=product.ProductName,
                        Quantity=item.Quantity,
                        Unit_price=product.Price,
                    )
                )

            orders_sv = OrdersService()
            new_order_id = orders_sv.create_order(user_id, newOrder, list_product)
            if not new_order_id:
                return JSONResponse(content={"message": "Created order failed"}, status_code=400)

            order_info = orders_sv.get_order_byID(new_order_id)
            order_details = orders_sv.get_order_details(new_order_id)

            return JSONResponse(
                content=jsonable_encoder({
                    "message": "Created order successfully",
                    "Order": order_info,
                    "Details": order_details,
                }),
                status_code=201,
            )

        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def delete_order(self, order_id: int):
        try:
            orders_sv = OrdersService()
            order = orders_sv.get_order_byID(order_id)
            if not order:
                return JSONResponse(
                    content=jsonable_encoder({
                        "message": f"OrderID {order_id} does not exist",
                    }),
                    status_code=404,
                )
            orders_sv.delete_order(order_id)
            return JSONResponse(
                content=jsonable_encoder({
                    "message": f"Delete order {order_id} successfully",
                }),
                status_code=201,
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
