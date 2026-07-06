"""
WAC Portal Endpoints
Public endpoints for B2B clients to view and interact with offers.
No authentication required - uses share_token for access.
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.wac_proxy import WacProxyService

router = APIRouter()


# ─── Schemas ─────────────────────────────────────────────────────────────────

class PortalOfferAcceptRequest(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None


class PortalOfferRejectRequest(BaseModel):
    reason: Optional[str] = None


class PortalBookingItemRequest(BaseModel):
    offer_item_id: int
    client_name: Optional[str] = None
    nationality: Optional[str] = None
    remarks: Optional[str] = None


class PortalBookingRequest(BaseModel):
    client_name: str
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    nationality: Optional[str] = None
    items: list[PortalBookingItemRequest] = []


# ─── Endpoints ───────────────────────────────────────────────────────────────

@router.get("/{tenant_slug}/offers/{share_token}")
async def view_offer_public(
    tenant_slug: str,
    share_token: str,
):
    """Vista pública de una oferta - sin autenticación."""
    try:
        result = await WacProxyService.proxy_request(
            "GET",
            f"/api/v1/public/{tenant_slug}/offers/{share_token}",
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching offer: {str(e)}")


@router.post("/{tenant_slug}/offers/{share_token}/accept")
async def accept_offer_public(
    tenant_slug: str,
    share_token: str,
    data: PortalOfferAcceptRequest,
):
    """Aceptar una oferta pública."""
    try:
        result = await WacProxyService.proxy_request(
            "POST",
            f"/api/v1/public/{tenant_slug}/offers/{share_token}/accept",
            json_data=data.model_dump(exclude_unset=True),
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error accepting offer: {str(e)}")


@router.post("/{tenant_slug}/offers/{share_token}/reject")
async def reject_offer_public(
    tenant_slug: str,
    share_token: str,
    data: PortalOfferRejectRequest,
):
    """Rechazar una oferta pública."""
    try:
        result = await WacProxyService.proxy_request(
            "POST",
            f"/api/v1/public/{tenant_slug}/offers/{share_token}/reject",
            json_data=data.model_dump(exclude_unset=True),
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error rejecting offer: {str(e)}")


@router.post("/{tenant_slug}/offers/{share_token}/book")
async def book_offer_public(
    tenant_slug: str,
    share_token: str,
    data: PortalBookingRequest,
):
    """Crear reserva(s) desde una oferta aceptada."""
    try:
        result = await WacProxyService.proxy_request(
            "POST",
            f"/api/v1/public/{tenant_slug}/offers/{share_token}/book",
            json_data=data.model_dump(exclude_unset=True),
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error booking offer: {str(e)}")
