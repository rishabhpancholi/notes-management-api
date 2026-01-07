from fastapi import (
    FastAPI,
    Request
)
from fastapi.responses import JSONResponse

def register_exception_handler(app: FastAPI)-> None:
    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception)-> None:
        return JSONResponse(
            status_code = 500,
            content = {
                "detail": str(exc)
            }
        )