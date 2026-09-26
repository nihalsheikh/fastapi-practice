from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Limiter Setup
limiter = Limiter(key_func=get_remote_address)

# save limiter in app state
app.state.limiter = limiter

# Error Handling for Rate Limit
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Too many requests"
        }
    )

# Count the times we hit an API
count = 0

# Rate Limited API
@app.get("/data", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def get_data(request: Request):
    global count
    count += 1

    return {"message": "Home Route with Rate Limit", "endpoint_hit_count": count}
