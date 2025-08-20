from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import Decimal
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import product_usecase
from store.core.exceptions import NotFoundException, BadRequestException


router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create(body: ProductIn = Body(...)) -> ProductOut:
    try:
        return await product_usecase.create(body=body)
    except BadRequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(id: UUID) -> ProductOut:
    try:
        return await product_usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    min_price: Decimal = Query(None, description="Minimum price filter"),
    max_price: Decimal = Query(None, description="Maximum price filter")
) -> List[ProductOut]:
    return await product_usecase.query(min_price=min_price, max_price=max_price)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(id: UUID, body: ProductUpdate = Body(...)) -> ProductUpdateOut:
    try:
        return await product_usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID):
    try:
        await product_usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
