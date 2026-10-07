from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from starlette.requests import Request

app = FastAPI()

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "caught by Exception"})

@app.get("/")
def read_root():
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Database offline"
    )

client = TestClient(app)
response = client.get("/")
print(response.status_code)
