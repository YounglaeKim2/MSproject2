from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SimpleRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    gender: str
    name: str

@router.post("/simple-test")
async def simple_test(data: SimpleRequest):
    return {
        "message": "데이터 수신 성공",
        "received": data.dict()
    }