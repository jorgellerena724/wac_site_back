"""
WAC Proxy Endpoints
Proxies authenticated requests from the site frontend to wac-back.
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from app.api.endpoints.token import verify_token, MockUser
from app.services.wac_proxy import WacProxyService

router = APIRouter()


class PricingRequest(BaseModel):
    hotel_id: Optional[int] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    room_type_id: Optional[int] = None
    board: str = "AI"
    adults: int = 2
    children: list = []
    infants: list = []
    use_revenue_intelligence: bool = False
    product_type: str = "hotel"


# ─── Pricing ─────────────────────────────────────────────────────────────────

@router.post("/pricing/hotel")
async def proxy_pricing_hotel(
    body: PricingRequest,
    current_user=Depends(verify_token),
):
    """Proxy hotel pricing to wac-back."""
    return await WacProxyService.proxy_request(
        "POST",
        "/api/v1/pricing/hotel",
        json_data=body.model_dump(exclude_unset=True),
    )


@router.post("/pricing/excursion")
async def proxy_pricing_excursion(
    body: dict,
    current_user=Depends(verify_token),
):
    """Proxy excursion pricing to wac-back."""
    return await WacProxyService.proxy_request(
        "POST",
        "/api/v1/pricing/excursion",
        json_data=body,
    )


@router.post("/pricing/transfer")
async def proxy_pricing_transfer(
    body: dict,
    current_user=Depends(verify_token),
):
    """Proxy transfer pricing to wac-back."""
    return await WacProxyService.proxy_request(
        "POST",
        "/api/v1/pricing/transfer",
        json_data=body,
    )


@router.post("/pricing/rent-car")
async def proxy_pricing_rent_car(
    body: dict,
    current_user=Depends(verify_token),
):
    """Proxy rent-car pricing to wac-back."""
    return await WacProxyService.proxy_request(
        "POST",
        "/api/v1/pricing/rent-car",
        json_data=body,
    )


@router.post("/pricing/tour-package")
async def proxy_pricing_tour_package(
    body: dict,
    current_user=Depends(verify_token),
):
    """Proxy tour-package pricing to wac-back."""
    return await WacProxyService.proxy_request(
        "POST",
        "/api/v1/pricing/tour-package",
        json_data=body,
    )


# ─── Availability ────────────────────────────────────────────────────────────

@router.get("/availability/hotels/{hotel_id}")
async def proxy_availability_hotel(
    hotel_id: int,
    check_in: str = Query(...),
    check_out: str = Query(...),
    current_user=Depends(verify_token),
):
    """Proxy hotel availability check to wac-back."""
    return await WacProxyService.proxy_request(
        "GET",
        f"/api/v1/availability/hotels/{hotel_id}",
        params={"check_in": check_in, "check_out": check_out},
    )


# ─── Tour Packages ───────────────────────────────────────────────────────────

@router.get("/tour-packages/")
async def proxy_list_tour_packages(
    status: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    offset: int = Query(0),
    limit: int = Query(50),
    current_user=Depends(verify_token),
):
    """Proxy tour package listing to wac-back."""
    params = {"offset": offset, "limit": limit}
    if status:
        params["status"] = status
    if is_active is not None:
        params["is_active"] = str(is_active).lower()
    if search:
        params["search"] = search

    return await WacProxyService.proxy_request(
        "GET",
        "/api/v1/tour-packages/",
        params=params,
    )


@router.get("/tour-packages/{package_id}/")
async def proxy_get_tour_package(
    package_id: int,
    current_user=Depends(verify_token),
):
    """Proxy single tour package to wac-back."""
    return await WacProxyService.proxy_request(
        "GET",
        f"/api/v1/tour-packages/{package_id}/",
    )
