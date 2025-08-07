from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import uuid

# 데이터베이스 및 모델 임포트
from . import models, database
from .database import engine

# 서비스 모듈 임포트
from .services.face_landmarker import get_face_landmarks
from .services.geometry_calculator import calculate_geometric_metrics
from .services.rule_engine import analyze_gwansang_rules
from .services.report_generator import generate_report
from .services.lucky_charm_generator import generate_lucky_charm_image

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI 관상 분석 API",
    description="사용자의 얼굴 이미지를 분석하여 전통 관상학에 기반한 해석을 제공합니다. **본 서비스는 오락용이며, 과학적 근거가 없습니다.**",
    version="1.1.0",
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from typing import Union, Tuple

def run_analysis_pipeline(image_path: str) -> Union[Tuple[str, str], None]:
    landmarks, height, width = get_face_landmarks(image_path)
    if not landmarks:
        return None
    geometric_metrics = calculate_geometric_metrics(landmarks, height, width)
    gwansang_keys = analyze_gwansang_rules(geometric_metrics)
    final_report, dalle_prompt = generate_report(gwansang_keys)
    return final_report, dalle_prompt

@app.post("/analyze/",
          summary="얼굴 이미지 관상 분석",
          description="**중요**: 이 엔드포인트는 오락 목적으로만 사용되어야 합니다.")
async def analyze_face_api(db: Session = Depends(database.get_db), file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="허용되지 않는 파일 형식입니다.")

    image_path = None  # image_path를 try 블록 밖에서 초기화
    try:
        filename = f"{uuid.uuid4()}_{file.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())

        analysis_result = run_analysis_pipeline(image_path)
        if analysis_result is None:
            raise HTTPException(status_code=400, detail="얼굴을 감지하지 못했습니다.")
        
        report, charm_prompt = analysis_result

        # 데이터베이스에 분석 결과 저장
        db_result = models.AnalysisResult(
            original_filename=file.filename,
            image_path=filename,
            report=report,
            lucky_charm_image_url=None  # 초기에는 부적 URL 없음
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)

        image_url = f"/uploads/{filename}"
        return JSONResponse(content={
            "success": True,
            "report": report,
            "analysis_id": db_result.id,
            "image_url": image_url,
            "charm_prompt": charm_prompt  # 프롬프트를 프론트엔드로 전달
        })

    except Exception as e:
        print(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=f"서버 내부 오류가 발생했습니다.")

from pydantic import BaseModel

class CharmRequest(BaseModel):
    prompt: str
    analysis_id: int

@app.post("/generate-charm/",
          summary="행운의 부적 생성",
          description="관상 분석 결과로 생성된 프롬프트를 사용하여 행운의 부적 이미지를 생성합니다.")
async def generate_charm_api(request: CharmRequest, db: Session = Depends(database.get_db)):
    try:
        lucky_charm_image_url = generate_lucky_charm_image(request.prompt)
        
        # DB에 부적 이미지 URL 업데이트
        db_result = db.query(models.AnalysisResult).filter(models.AnalysisResult.id == request.analysis_id).first()
        if db_result:
            db_result.lucky_charm_image_url = lucky_charm_image_url
            db.commit()

        return JSONResponse(content={
            "success": True,
            "lucky_charm_image_url": lucky_charm_image_url
        })
    except Exception as e:
        print(f"행운의 부적 이미지 생성 실패: {e}")
        raise HTTPException(status_code=500, detail="행운의 부적 이미지 생성에 실패했습니다.")

@app.get("/analysis-history/",
         summary="관상 분석 기록 조회",
         description="지금까지 수행된 관상 분석 기록을 최신순으로 조회합니다.")
def get_analysis_history(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 10):
    history = db.query(models.AnalysisResult).order_by(models.AnalysisResult.created_at.desc()).offset(skip).limit(limit).all()
    return history

@app.get("/", include_in_schema=False)
async def read_root():
    return FileResponse('static/index.html')
