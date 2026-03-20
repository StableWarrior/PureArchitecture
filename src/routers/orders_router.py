from uuid import UUID

from fastapi import APIRouter

from ..database.models import Order
from ..schemas import OrderRequest, OrderResponse, PaymentCallbackResponse
from ..usecases.order_create import OrderCreateUseCase
from ..usecases.order_get import OrderGetUseCase
from ..usecases.order_update import OrderUpdateUseCase

router = APIRouter(
    prefix="/api",
    tags=["orders"],
)


@router.post(
    "/orders", name="create_order", response_model=OrderResponse, status_code=201
)
async def create_order(order: OrderRequest) -> Order:
    result = await OrderCreateUseCase.create_order(order=order)
    return result


@router.post("/orders/payment-callback", name="update_order")
async def update_order(payment: PaymentCallbackResponse):
    await OrderUpdateUseCase.update_order(payment=payment)


@router.get("/orders/{order_id}", name="get_order", response_model=OrderResponse)
async def get_order(order_id: UUID) -> Order:
    result = await OrderGetUseCase.get_order(order_id=order_id)
    return result
