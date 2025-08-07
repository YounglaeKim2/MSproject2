#!/usr/bin/env python3
"""Import 테스트 스크립트"""
import sys
import os

# 경로 설정
sys.path.insert(0, os.getcwd())

def test_imports():
    """모든 import 테스트"""
    print("=== Import 테스트 시작 ===")
    
    # 1. 기본 services 테스트
    try:
        from app.services.saju_analyzer import saju_analyzer
        print("✓ saju_analyzer 성공")
    except Exception as e:
        print(f"✗ saju_analyzer 실패: {e}")
        return False
    
    try:
        from app.services.gemini_ai_interpreter import get_gemini_interpreter
        print("✓ gemini_ai_interpreter 성공")
    except Exception as e:
        print(f"✗ gemini_ai_interpreter 실패: {e}")
        return False
    
    # 2. Azure AI 테스트
    try:
        from app.services.azure_ai_interpreter import AzureOpenAIInterpreter
        print("✓ azure_ai_interpreter 성공")
        azure_available = True
    except Exception as e:
        print(f"✗ azure_ai_interpreter 실패: {e}")
        azure_available = False
    
    # 3. AI 서비스 선택기 테스트
    try:
        from app.services.ai_service_selector import get_ai_interpreter
        print("✓ ai_service_selector 성공")
        selector_available = True
    except Exception as e:
        print(f"✗ ai_service_selector 실패: {e}")
        selector_available = False
    
    # 4. API import 테스트
    try:
        from app.api import saju
        print("✓ saju API 성공")
    except Exception as e:
        print(f"✗ saju API 실패: {e}")
        return False
    
    # 5. FastAPI app 생성 테스트
    try:
        from app.main import app
        print("✓ FastAPI app 생성 성공")
    except Exception as e:
        print(f"✗ FastAPI app 생성 실패: {e}")
        return False
    
    print("\n=== 테스트 결과 ===")
    print(f"기본 기능: 사용 가능")
    print(f"Azure AI: {'사용 가능' if azure_available else '사용 불가'}")
    print(f"AI 선택기: {'사용 가능' if selector_available else '사용 불가'}")
    
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n모든 기본 import 성공! 서버 시작 가능")
    else:
        print("\n기본 import 실패! 서버 시작 불가")
        sys.exit(1)