import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.all(),
            'details': 'You are great trader!'
        }
    except ZeroDivisionError:
        raise HTTPException(status_code=500, detail={
            'status': 'success',
            'data': None,
            'details': 'You are great trader!'
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'Error',
            'data': None,
            'details': None
        })


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/long operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return 'Много времени требуется для вычислений'