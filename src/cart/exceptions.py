from fastapi import HTTPException


async def handle_exceptions(e: Exception):
    print(f"Unexpected Error: {e}")
    raise HTTPException(status_code=500, detail={"status": "error", "data": None, "details": str(e)})