"""
WAC Backend Proxy Service
Proxies requests from wac-site-back to wac-back for travel functionality.
"""
import httpx
import logging
from typing import Optional, Dict, Any
from app.config.config import settings

logger = logging.getLogger(__name__)


class WacProxyService:
    """Service to proxy requests to wac-back (travel SaaS backend)."""

    _client: Optional[httpx.AsyncClient] = None

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.AsyncClient(
                base_url=settings.WAC_BACKEND_URL,
                timeout=30.0,
                headers={"Content-Type": "application/json"},
            )
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client and not cls._client.is_closed:
            await cls._client.aclose()
            cls._client = None

    @staticmethod
    async def proxy_request(
        method: str,
        path: str,
        token: Optional[str] = None,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Forward a request to wac-back."""
        client = await WacProxyService.get_client()
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = await client.request(
                method,
                path,
                json=json_data,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                "WAC proxy HTTP error: %s %s -> %s: %s",
                method, path, e.response.status_code, e.response.text[:200],
            )
            raise
        except httpx.RequestError as e:
            logger.error("WAC proxy request error: %s %s -> %s", method, path, str(e))
            raise

    @staticmethod
    async def proxy_request_raw(
        method: str,
        path: str,
        token: Optional[str] = None,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Forward a request and return the raw response."""
        client = await WacProxyService.get_client()
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = await client.request(
            method,
            path,
            json=json_data,
            params=params,
            headers=headers,
        )
        return response
