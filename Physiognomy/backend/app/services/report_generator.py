

# report_generator.py
import os
from typing import List, Dict

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI

# 1. 지식 베이스(KB) 및 RAG 파이프라인 설정
def initialize_rag_pipeline():
    """
    '관상로직.txt'를 로드하여 RAG 파이프라인을 초기화하고 QA 체인을 반환합니다.
    """
    kb_file_path = "/app/관상로직.txt"
    if not os.path.exists(kb_file_path):
        raise FileNotFoundError(f"지식 베이스 파일을 찾을 수 없습니다: {kb_file_path}")

    with open(kb_file_path, 'r', encoding='utf-8') as f:
        knowledge_base_text = f.read()

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_text(knowledge_base_text)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts, embeddings)
    # 환경변수에서 Google API 키와 모델명 가져오기
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    llm = GoogleGenerativeAI(
        google_api_key=google_api_key,
        model=model_name,
        temperature=0.7
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

# 전역 변수로 QA 체인 초기화
try:
    QA_CHAIN = initialize_rag_pipeline()
except Exception as e:
    print(f"RAG 파이프라인 초기화 실패: {e}")
    QA_CHAIN = None

# 2. 해석 키를 한글 특징명으로 변환하는 매핑
KEY_TO_FEATURE_MAP: Dict[str, str] = {
    "FACE_SHAPE_ROUND": "둥근 얼굴형",
    "FACE_SHAPE_LONG": "긴 얼굴형",
    "FACE_SHAPE_BALANCED": "균형 잡힌 얼굴형",
    "FOREHEAD_WIDE": "넓고 높은 이마",
    "FOREHEAD_NARROW": "좁은 이마",
    "FOREHEAD_BALANCED": "조화로운 이마",
    "EYES_SPACED_WIDE": "눈 사이가 넓은 편",
    "EYES_SPACED_NARROW": "눈 사이가 좁은 편",
    "EYES_SPACED_BALANCED": "조화로운 눈 간격",
    "NOSE_PROMINENT": "높고 뚜렷한 코",
    "NOSE_WIDE": "복코 (풍성한 콧방울)",
    "LIPS_THICK": "도톰한 입술",
    "MOUTH_CORNERS_UP": "올라간 입꼬리",
    "MOUTH_CORNERS_DOWN": "처진 입꼬리"
}



def generate_report(interpretation_keys: List[str]) -> str:
    """
    해석 키 리스트를 받아 RAG 기반의 종합적인 텍스트 리포트를 생성합니다.
    """
    if not interpretation_keys:
        return "얼굴 특징을 분석할 수 없습니다. 다른 사진으로 시도해보세요."
        
    if QA_CHAIN is None:
        return "답변 생성 시스템에 오류가 발생했습니다. 관리자에게 문의하세요."

    # 감지된 특징들을 한글 문자열로 변환
    detected_features = [KEY_TO_FEATURE_MAP.get(key, key) for key in interpretation_keys]
    features_str = ", ".join(detected_features)

    # AI 모델에 전달할 종합 분석용 프롬프트
    prompt = f"""
    당신은 사용자의 자신감을 북돋아주는 매우 친절하고 유능한 관상 전문가입니다.
    
    사용자의 얼굴에서 다음과 같은 특징들이 감지되었습니다: **{features_str}**
    
    이 특징들을 개별적으로 설명하지 말고, **하나의 완성된 이야기처럼 유기적으로 연결하여 종합적인 관상 풀이**를 작성해주세요. 각 특징이 서로 어떻게 영향을 미치는지, 예를 들어 초년운, 중년운, 말년운의 흐름이나 성격, 재물, 직업운의 관계를 종합적으로 분석하여 깊이 있는 통찰을 제공해주세요.
    
    답변은 다음 형식을 따라주세요:
    1.  [총평]: 전체적인 인상과 운의 흐름을 요약하여 전달합니다.
    2.  [상세 분석]: 각 특징을 서로 연결지어 상세한 스토리텔링 형식으로 풀어 설명합니다. 긍정적인 측면을 부각하고, 보완할 점이 있다면 부드럽고 희망적인 조언을 덧붙여주세요.
    3.  [성공을 위한 조언]: 분석 결과를 바탕으로, 사용자가 자신의 잠재력을 최대한 발휘하고 더 나은 삶을 살아갈 수 있도록 구체적이고 실천적인 조언을 1~2가지 제안합니다.
    
    전체적으로 매우 긍정적이고 희망적인 메시지를 전달하는 것을 잊지 마세요.
    '관상로직.txt'의 내용을 기반으로 답변을 생성하되, 내용을 그대로 가져오지 말고 자연스럽게 재구성해주세요.
    """

    try:
        if QA_CHAIN is not None:
            # QA 체인을 한 번만 실행하여 종합 리포트 생성
            result = QA_CHAIN.invoke({"query": prompt})
            comprehensive_report = result.get("result", "종합적인 관상 분석 결과를 생성하는 데 실패했습니다.")
        else:
            # RAG 파이프라인이 실패한 경우 기본 Google Gemini API 직접 사용
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if google_api_key:
                from langchain_google_genai import GoogleGenerativeAI
                llm = GoogleGenerativeAI(
                    google_api_key=google_api_key,
                    model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
                    temperature=0.7
                )
                comprehensive_report = llm.invoke(prompt)
            else:
                comprehensive_report = f"감지된 특징: {features_str}\n\n기본 관상 분석이 완료되었습니다. AI 해석 기능은 현재 준비 중입니다."
        
        report_parts = ["### 💎 AI 관상 종합 분석 리포트 💎\n\n"]
        report_parts.append(comprehensive_report)

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in generate_report: {e}")
        print(f"TRACEBACK: {error_trace}")
        return f"답변 생성 시스템에 오류가 발생했습니다. 관리자에게 문의하세요."

    
    
    # 최종 고지사항 추가
    report_parts.append("\n\n---\n")
    report_parts.append("※ 본 분석은 전통 관상학 정보를 기반으로 한 AI 생성 콘텐츠이며, 재미와 자기 성찰을 위한 참고 자료입니다. 과학적 근거나 절대적인 판단 기준으로 사용될 수 없습니다. ※")

    return "\n".join(report_parts)

# --- 테스트용 코드 ---
if __name__ == '__main__':
    if "GOOGLE_API_KEY" not in os.environ:
        print("오류: GOOGLE_API_KEY 환경 변수를 설정해주세요.")
    else:
        print("RAG 파이프라인을 초기화하는 중입니다. 잠시만 기다려주세요...")
        test_keys = [
            "FACE_SHAPE_ROUND",
            "FOREHEAD_WIDE",
            "NOSE_WIDE",
            "MOUTH_CORNERS_UP"
        ]
        print(f"\n테스트 키: {test_keys}")
        print("\n리포트를 생성합니다...\n")
        final_report = generate_report(test_keys)
        print(final_report)
