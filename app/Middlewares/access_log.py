
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.lifespan import logger


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"
        request_id = getattr(request.state, "request_id", "-")

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.exception(
                "Request failed | request_id={} | client={} | method={} | path={} | duration_ms={} | error={}",
                request_id,
                client_host,
                request.method,
                request.url.path,
                duration_ms,
                exc,
            )
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "Request completed | request_id={} | client={} | method={} | path={} | status_code={} | duration_ms={}",
            getattr(request.state, "request_id", request_id),
            client_host,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response