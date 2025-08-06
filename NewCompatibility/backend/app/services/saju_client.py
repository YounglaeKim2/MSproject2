"""
SAJU API 클라이언트 서비스
- 기존 SAJU API (포트 8000)와 HTTP 통신
- 개인 사주 분석 결과 받아오기
- 에러 핸들링 및 재시도 로직
"""
import httpx
import logging
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class SajuAPIClient:
    """SAJU API 클라이언트"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30.0
        
    async def check_health(self) -> Dict[str, Any]:
        """SAJU API 헬스 체크"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return {
                    "status": "healthy",
                    "saju_api_response": response.json(),
                    "response_time": response.elapsed.total_seconds() if response.elapsed else 0
                }
        except httpx.TimeoutException:
            logger.error("SAJU API 헬스 체크 타임아웃")
            return {"status": "timeout", "error": "SAJU API 응답 시간 초과"}
        except httpx.ConnectError:
            logger.error("SAJU API 연결 실패")
            return {"status": "disconnected", "error": "SAJU API 서버에 연결할 수 없습니다"}
        except Exception as e:
            logger.error(f"SAJU API 헬스 체크 실패: {e}")
            return {"status": "error", "error": str(e)}
    
    async def analyze_saju(self, birth_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        개인 사주 분석 요청
        
        Args:
            birth_info: {
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 14,
                "gender": "male",
                "name": "홍길동"
            }
        
        Returns:
            완전한 사주 분석 결과
        """
        try:
            logger.info(f"SAJU API 호출 시작: {birth_info.get('name', 'Unknown')}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/saju/analyze",
                    json=birth_info
                )
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"SAJU API 호출 성공: {birth_info.get('name', 'Unknown')}")
                
                return {
                    "success": True,
                    "data": result,
                    "response_time": response.elapsed.total_seconds() if response.elapsed else 0,
                    "timestamp": datetime.now().isoformat()
                }
                
        except httpx.TimeoutException:
            error_msg = f"SAJU API 타임아웃: {birth_info.get('name', 'Unknown')}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": "timeout",
                "message": "사주 분석 요청이 시간 초과되었습니다",
                "details": error_msg
            }
            
        except httpx.HTTPStatusError as e:
            error_msg = f"SAJU API HTTP 오류 {e.response.status_code}: {birth_info.get('name', 'Unknown')}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": "http_error",
                "status_code": e.response.status_code,
                "message": "사주 분석 요청 중 오류가 발생했습니다",
                "details": error_msg
            }
            
        except httpx.ConnectError:
            error_msg = f"SAJU API 연결 실패: {birth_info.get('name', 'Unknown')}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": "connection_error",
                "message": "SAJU API 서버에 연결할 수 없습니다",
                "details": error_msg
            }
            
        except Exception as e:
            error_msg = f"SAJU API 호출 실패: {birth_info.get('name', 'Unknown')} - {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": "unknown_error",
                "message": "예상치 못한 오류가 발생했습니다",
                "details": error_msg
            }
    
    async def analyze_multiple_saju(self, person1_info: Dict[str, Any], person2_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        두 사람의 사주 분석 (궁합용)
        
        Args:
            person1_info: 첫 번째 사람 출생정보
            person2_info: 두 번째 사람 출생정보
        
        Returns:
            두 사람의 사주 분석 결과
        """
        try:
            logger.info("두 사람 사주 분석 시작")
            
            # 두 API 호출을 병렬로 실행
            person1_task = self.analyze_saju(person1_info)
            person2_task = self.analyze_saju(person2_info)
            
            person1_result, person2_result = await asyncio.gather(
                person1_task, person2_task, return_exceptions=True
            )
            
            # 결과 검증
            if isinstance(person1_result, Exception):
                logger.error(f"Person1 분석 실패: {person1_result}")
                return {
                    "success": False,
                    "error": "person1_analysis_failed",
                    "message": f"{person1_info.get('name', '첫 번째 사람')} 사주 분석에 실패했습니다",
                    "details": str(person1_result)
                }
            
            if isinstance(person2_result, Exception):
                logger.error(f"Person2 분석 실패: {person2_result}")
                return {
                    "success": False,
                    "error": "person2_analysis_failed",
                    "message": f"{person2_info.get('name', '두 번째 사람')} 사주 분석에 실패했습니다",
                    "details": str(person2_result)
                }
            
            if not person1_result.get("success", False):
                return {
                    "success": False,
                    "error": "person1_analysis_failed",
                    "message": f"{person1_info.get('name', '첫 번째 사람')} 사주 분석에 실패했습니다",
                    "details": person1_result.get("message", "Unknown error")
                }
            
            if not person2_result.get("success", False):
                return {
                    "success": False,
                    "error": "person2_analysis_failed", 
                    "message": f"{person2_info.get('name', '두 번째 사람')} 사주 분석에 실패했습니다",
                    "details": person2_result.get("message", "Unknown error")
                }
            
            logger.info("두 사람 사주 분석 완료")
            
            return {
                "success": True,
                "person1": person1_result["data"],
                "person2": person2_result["data"],
                "analysis_info": {
                    "person1_name": person1_info.get("name", "Person1"),
                    "person2_name": person2_info.get("name", "Person2"),
                    "analysis_time": datetime.now().isoformat(),
                    "response_times": {
                        "person1": person1_result.get("response_time", 0),
                        "person2": person2_result.get("response_time", 0)
                    }
                }
            }
            
        except Exception as e:
            error_msg = f"두 사람 사주 분석 실패: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": "multiple_analysis_failed",
                "message": "두 사람의 사주 분석 중 오류가 발생했습니다",
                "details": error_msg
            }

# 글로벌 인스턴스
saju_client = SajuAPIClient()
