from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/")
async def home():
    await asyncio.sleep(3)
    return { "message": "Text appears after 3 sec" }


# ---------- Normal Sync and Async Program ------------------
# import asyncio
# import time

# # Normal syncronous program
# def time_count():
#     time.sleep(3) # 3 seconds
#     return "Sleep in 3 sec..."


# # Async Program
# async def time_count_2():
#     await asyncio.sleep(3)
#     return "Sleep in 3 sec..."
