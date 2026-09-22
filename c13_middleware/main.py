from fastapi import FastAPI, status, Request
import time

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Home Route"}

@app.middleware("http")
async def log_middleware(req: Request, call_next):
    print("Request via middleware")

    start_time = time.time()
    print(f"Time: {start_time}")

    response = await call_next(req)

    process_time = time.time() - start_time

    print("\nResponse via middleware")

    print(f"Time: {process_time}")

    print(f"\nPath: {req.url.path} | Time: {process_time}")

    return response
