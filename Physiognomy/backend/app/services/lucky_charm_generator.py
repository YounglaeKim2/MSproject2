import os
import requests
from datetime import datetime
from openai import AzureOpenAI

# Azure OpenAI 클라이언트 초기화
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# 이미지 저장 디렉토리 설정
IMAGE_DIR = "app/static/amulets"
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_lucky_charm_image(prompt: str) -> str:
    """
    Azure DALL-E API를 사용하여 행운의 부적 이미지를 생성하고 저장합니다.

    Args:
        prompt (str): 이미지 생성을 위한 DALL-E 프롬프트

    Returns:
        str: 생성된 이미지의 URL
    """
    try:
        result = client.images.generate(
            model=os.getenv("AZURE_OPENAI_DALLE_DEPLOYMENT"), # DALL-E 3 모델의 배포 이름 사용
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = result.data[0].url

        if not image_url:
            raise ValueError("API 응답에서 이미지 URL을 찾을 수 없습니다.")

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
