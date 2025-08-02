import os
import openai
import requests
from datetime import datetime

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 이미지 저장 디렉토리 설정
IMAGE_DIR = "app/static/amulets"
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_lucky_charm_image(prompt: str) -> str:
    """
    DALL-E API를 사용하여 행운의 부적 이미지를 생성하고 저장합니다.

    Args:
        prompt (str): 이미지 생성을 위한 DALL-E 프롬프트

    Returns:
        str: 생성된 이미지의 URL
    """
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # 이미지 다운로드
        image_data = requests.get(image_url).content
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"lucky_charm_{timestamp}.png"
        filepath = os.path.join(IMAGE_DIR, filename)
        
        # 이미지 저장
        with open(filepath, "wb") as f:
            f.write(image_data)
            
        return f"/static/amulets/{filename}"

    except Exception as e:
        print(f"DALL-E 이미지 생성 실패: {e}")
        return None