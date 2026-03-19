from fastapi import APIRouter
from uuid import UUID
from ..usecases.order_create import OrderCreateUseCase
from ..usecases.order_get import OrderGetUseCase
from ..schemas import OrderResponse, OrderRequest
from ..database.models import Order
router = APIRouter(
    prefix="/api",
    tags=["orders"],
)

@router.post("/orders", name="create_order", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderRequest) -> Order:
    result = await OrderCreateUseCase.create_order(order=order)
    return result

@router.get("/orders/{order_id}", name="get_order", response_model=OrderResponse)
async def get_order(order_id: UUID) -> Order:
    result = await OrderGetUseCase.get_order(order_id=order_id)
    return result
