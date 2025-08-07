from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import traceback
from app.api import saju

class UnicodeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

app = FastAPI(
    title="사주 웹 서비스 API",
    description="사주팔자 분석 및 해석 서비스",
    version="1.0.0",
    default_response_class=UnicodeJSONResponse
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React 개발 서버 (기존)
        "http://localhost:4000",  # Vite 개발 서버
        "http://localhost:4001",  # Vite 개발 서버 (포트 변경)
        "http://192.168.219.141:8000",  # 모바일 앱 네트워크 접근
        "*",  # 모바일 개발 중 모든 origins 허용 (임시)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 글로벌 에러 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"=== 글로벌 에러 핸들러 ===")
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Error: {str(exc)}")
    print(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"서버 오류: {str(exc)}"}
    )

# API 라우터 등록
app.include_router(saju.router, prefix="/api/v1/saju", tags=["saju"])

# Azure OpenAI API 라우터 등록 (안전한 try-catch)
try:
    from app.api.azure_api import azure_router
    app.include_router(azure_router, prefix="/api/v1/azure", tags=["azure"])
    print("Azure OpenAI API router registered successfully")
except ImportError as e:
    print(f"Azure OpenAI API router load failed: {e}")
    print("Only Gemini AI is available")
except Exception as e:
    print(f"Azure OpenAI API router registration failed: {e}")

@app.get("/")
async def root():
    return {"message": "사주 웹 서비스 API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

