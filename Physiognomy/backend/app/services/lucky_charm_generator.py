
import os
from openai import AzureOpenAI
import json

def generate_lucky_charm_image(prompt: str) -> str:
    """
    DALL-E 3를 사용하여 주어진 프롬프트로 행운의 부적 이미지를 생성합니다.
    """
    try:
        client = AzureOpenAI(
            api_version=os.environ["OPENAI_API_VERSION"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
        )

        result = client.images.generate(
            model=os.environ["AZURE_OPENAI_DALLE_DEPLOYMENT"],
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        return image_url

    except KeyError as e:
        raise Exception(f"환경 변수 오류: {e}를 찾을 수 없습니다. .env 파일을 확인해주세요.")
    except Exception as e:
        print(f"DALL-E 3 이미지 생성 중 오류 발생: {e}")
        raise
