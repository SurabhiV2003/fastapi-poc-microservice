import time
import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .database import SessionLocal
from . import crud

# Set up structured logging to the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Capture Request Data
        path = request.url.path
        method = request.method
        
        # We try to get the body, but carefully as it's a stream
        request_body = ""
        if method == "POST":
            body_bytes = await request.body()
            request_body = body_bytes.decode("utf-8") if body_bytes else ""
            # Re-wrap the body so the actual endpoint can still read it
            async def receive():
                return {"type": "http.request", "body": body_bytes}
            request._receive = receive

        # 2. Process the request and measure time
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # 3. Capture Response Data
        status_code = response.status_code
        
        # To capture the response body, we have to iterate through the response iterator
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        # Since we consumed the iterator, we must recreate it for the client
        from starlette.responses import Response
        response = Response(
            content=response_body,
            status_code=status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )

        # 4. Save to Audit Log (Database)
        db = SessionLocal()
        try:
            crud.create_audit_log(
                db=db,
                endpoint=f"{method} {path}",
                request_payload=request_body,
                response_payload=response_body.decode("utf-8") if response_body else "",
                status_code=status_code
            )
            
            # 5. Structured Log to Terminal
            log_data = {
                "method": method,
                "path": path,
                "status": status_code,
                "duration": f"{process_time:.4f}s"
            }
            logger.info(json.dumps(log_data))
            
        finally:
            db.close()

        return response