

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
    # 얼굴형 (Face Shape)
    "FACE_SHAPE_ROUND": "둥근 얼굴형 (원형)",
    "FACE_SHAPE_SQUARE": "사각형 얼굴형 (전형)",
    "FACE_SHAPE_LONG": "긴 얼굴형 (동자형)",
    "FACE_SHAPE_INVERTED_TRIANGLE": "역삼각형 얼굴형 (V라인)",
    "FACE_SHAPE_EGG": "계란형 얼굴형",

    # 이마 (Forehead)
    "FOREHEAD_WIDE_HIGH": "넓고 높은 이마",
    "FOREHEAD_NARROW": "좁은 이마",
    "FOREHEAD_ROUNDED": "둥근 이마",
    "FOREHEAD_ANGULAR": "각진 이마",
    "FOREHEAD_M_SHAPE": "M자형 이마",

    # 눈 (Eyes)
    "EYES_LARGE": "큰 눈",
    "EYES_SMALL": "작은 눈",
    "EYES_UPWARD_SLANTING": "올라간 눈꼬리",
    "EYES_DOWNWARD_SLANTING": "처진 눈꼬리",
    "EYES_ASYMMETRICAL": "짝눈 (자웅안)",
    "EYES_MONOLID": "외꺼풀 눈",
    "EYES_DOUBLE_LID": "쌍꺼풀 눈",
    "EYES_SPACED_WIDE": "눈 사이가 넓은 편 (미간 넓음)",
    "EYES_SPACED_NARROW": "눈 사이가 좁은 편 (미간 좁음)",

    # 눈썹 (Eyebrows)
    "EYEBROWS_LONG": "긴 눈썹 (눈보다 김)",
    "EYEBROWS_SHORT": "짧은 눈썹 (눈보다 짧음)",
    "EYEBROWS_THICK": "진하고 숱 많은 눈썹",
    "EYEBROWS_THIN": "옅고 숱 없는 눈썹",
    "EYEBROWS_STRAIGHT": "일자 눈썹",
    "EYEBROWS_CRESCENT": "초승달 눈썹",
    "EYEBROWS_UPWARD": "올라간 눈썹 (장군형)",
    "EYEBROWS_DOWNWARD": "처진 눈썹 (팔자형)",
    "EYEBROWS_BROKEN": "끊어진 눈썹",
    "EYEBROWS_CONNECTED": "이어진 눈썹",

    # 코 (Nose)
    "NOSE_LARGE": "크고 높은 코",
    "NOSE_SMALL": "작은 코",
    "NOSE_LONG": "긴 코",
    "NOSE_SHORT": "짧은 코",
    "NOSE_WIDE_WINGS": "복코 (콧방울이 넓고 풍성함)",
    "NOSE_ROUNDED_TIP": "둥근 코끝",
    "NOSE_POINTED_TIP": "뾰족한 코끝",
    "NOSE_UPTURNED": "들창코 (콧구멍 보임)",

    # 광대뼈 (Cheekbones)
    "CHEEKBONES_PROMINENT": "돌출된 광대뼈",
    "CHEEKBONES_BALANCED": "균형 잡힌 광대뼈",

    # 입술 및 입 (Lips & Mouth)
    "LIPS_THICK": "도톰한 입술",
    "LIPS_THIN": "얇은 입술",
    "MOUTH_LARGE": "큰 입",
    "MOUTH_SMALL": "작은 입",
    "MOUTH_CORNERS_UP": "올라간 입꼬리",
    "MOUTH_CORNERS_DOWN": "처진 입꼬리",
    "LIPS_UPPER_THICKER": "윗입술이 더 두꺼운 입술",
    "LIPS_LOWER_THICKER": "아랫입술이 더 두꺼운 입술",

    # 턱 (Chin/Jaw)
    "JAW_WIDE_THICK": "넓고 두툼한 턱",
    "JAW_POINTED_VLINE": "뾰족한 V라인 턱",
    "JAW_SQUARE": "사각턱",
    "JAW_PROTRUDING": "주걱턱",
    "JAW_RECEDING": "무턱",

    # 귀 (Ears)
    "EARS_LARGE": "큰 귀",
    "EARS_SMALL": "작은 귀",
    "EARS_THICK_LOBE": "두툼한 귓불 (복귀)",
    "EARS_THIN_LOBE": "얇거나 없는 귓불",
    "EARS_POINTED_TOP": "윗부분이 뾰족한 귀 (칼귀)",
    "EARS_ROUNDED_TOP": "윗부분이 둥근 귀",

    # 인중 (Philtrum)
    "PHILTRUM_LONG": "긴 인중",
    "PHILTRUM_SHORT": "짧은 인중",
    "PHILTRUM_DEEP": "깊은 인중",
    "PHILTRUM_SHALLOW": "얕은 인중",
    "PHILTRUM_WIDE": "넓은 인중",
    "PHILTRUM_NARROW": "좁은 인중",

    # 법령 (Nasolabial Folds)
    "NASOLABIAL_CLEAR_LONG": "선명하고 긴 법령 (팔자주름)",
    "NASOLABIAL_FAINT_SHORT": "희미하고 짧은 법령 (팔자주름)",
    "NASOLABIAL_ENTERING_MOUTH": "입으로 들어가는 법령 (등사입구)"
}



def generate_report(interpretation_keys: List[str]) -> str:
    """
    해석 키 리스트를 받아 AI 모델을 직접 호출하여 종합적인 텍스트 리포트를 생성합니다.
    """
    if not interpretation_keys:
        return "얼굴 특징을 분석할 수 없습니다. 다른 사진으로 시도해보세요."

    # 감지된 특징들을 한글 문자열로 변환
    detected_features = [KEY_TO_FEATURE_MAP.get(key, key) for key in interpretation_keys]
    features_str = ", ".join(detected_features)

    # AI 모델에 전달할 종합 분석용 프롬프트
    prompt = f"""
        당신은 사용자의 자신감을 북돋아주는 매우 친절하고 유능한 관상 전문가입니다. 당신의 목표는 운명을 단정 짓는 것이 아니라, 사용자가 자신의 잠재력을 발견하고 긍정적인 방향으로 나아갈 수 있도록 돕는 따뜻한 조언자입니다.

        사용자의 얼굴에서 다음과 같은 특징들이 감지되었습니다: **{features_str}**

        이 특징들을 개별적으로 설명하지 말고, **하나의 완성된 이야기처럼 유기적으로 연결하여 종합적인 관상 풀이**를 작성해주세요. 각 특징이 서로 어떻게 영향을 미치는지, 예를 들어 초년운, 중년운, 말년운의 흐름이나 성격, 재물, 직업운의 관계를 종합적으로 분석하여 깊이 있는 통찰을 제공해주세요.

        ### 분석 시 고려할 관점:
        1.  **오행(五行) 분석**: 감지된 얼굴형을 바탕으로 사용자의 대표적인 오행(예: 목형(木形), 화형(火形), 토형(土形), 금형(金形), 수형(水形))을 파악하고, 그에 따른 타고난 기질과 재능을 분석의 시작점으로 삼아주세요.
        2.  **삼정(三停)의 균형**: 이마(상정), 코와 광대(중정), 턱(하정)의 비율과 발달 정도를 통해 초년, 중년, 말년운의 전체적인 흐름과 강약을 설명해주세요.
        3.  **십이궁(十二宮)과 연결**: 주요 특징들을 관련된 궁(예: 코-재백궁(재물), 이마-관록궁(직업), 눈썹-형제궁(대인관계))과 연결하여 구체적인 삶의 영역에 대한 해석을 더해주세요.
        4.  **특징 간의 조화**: 서로 다른 특징들이 어떻게 조화를 이루거나 서로를 보완하는지 설명해주세요. (예: "추진력을 상징하는 발달된 광대뼈를 가지고 있지만, 신중함을 나타내는 차분한 눈매가 이를 균형 있게 잡아주어, 당신은 대담하면서도 실수가 적은 리더의 자질을 갖추고 있습니다.")

        ### 재미와 흥미를 더하는 분석:
        *   **유사 유명인/동물상 비유**: 분석 내용과 어울리는 유명인이나 동물상(예: 강아지상, 고양이상)에 긍정적으로 비유하여 사용자가 자신의 매력을 더 쉽게 이해하고 즐길 수 있도록 해주세요. [1]
        *   **숨겨진 매력 포인트**: 사용자가 미처 몰랐을 수 있는, 관상학적으로 나타나는 숨겨진 매력이나 재능을 한 가지 짚어주세요.

        답변은 다음 형식을 반드시 따라주세요:

        1.  **[총평]**: 전체적인 인상과 운의 흐름, 그리고 당신이 가진 가장 큰 강점을 한두 문장으로 요약하여 전달합니다.
        2.  **[인생의 황금기와 시간의 흐름]**: 삼정 분석을 바탕으로 당신의 인생에서 가장 빛날 시기는 언제이며, 시간의 흐름에 따라 운세가 어떻게 변화하는지 알려줍니다.
        3.  **[상세 분석: 타고난 성격과 잠재력]**: 오행 기운과 얼굴의 각 특징을 종합하여 당신의 타고난 성격, 강점, 그리고 숨겨진 잠재력에 대해 깊이 있게 설명합니다.
        4.  **[사회생활과 인간관계]**: 눈썹, 광대, 입 등을 통해 당신의 사회적 성향과 대인관계의 특징을 분석하고, 더 나은 관계를 위한 팁을 제공합니다.
        5.  **[재물운과 직업운]**: 코(재백궁)와 이마(관록궁)를 중심으로 당신의 재물운과 성공 가능성이 높은 직업 분야에 대해 이야기합니다.
        6.  **[성공을 위한 조언]**: 분석 결과를 바탕으로, 당신의 잠재력을 최대한 발휘하고 더 나은 삶을 살아갈 수 있도록 구체적이고 실천 가능한 조언을 1~2가지 제안합니다.
        7.  **[당신을 위한 행운의 메시지]**: 당신의 오행 기운에 맞는 행운의 색상이나 아이템을 추천하고, 힘이 되는 짧은 명언을 함께 전달합니다.
        8. **[유명인/동물상]**: 당신의 특징과 잘 어울리는 유명인이나 동물상을 비유로 들어, 당신의 매력을 강조합니다.
        9. **[숨겨진 매력 포인트]**: 당신이 미처 몰랐을 수 있는 숨겨진 매력이나 재능을 한 가지 짚어주세요.


        전체적으로 매우 긍정적이고 희망적인 메시지를 전달하는 것을 잊지 마세요.
        '관상로직.txt'의 내용을 기반으로 답변을 생성하되, 내용을 그대로 가져오지 말고 자연스럽게 재구성해주세요.

        답변에 별표(*)를 사용하지 마세요.

        글씨를 굵게 표시하지 마세요.

        일반 텍스트로만 답변해 주세요.

        마크다운 서식 없이 답변해 줘.

        핵심 단어 강조를 위한 별표(*) 사용을 최소화해 줘.

        답변에 # 문자를 사용하지 마세요.
    """

    try:
        # RAG 파이프라인을 우회하고 항상 Google Gemini API를 직접 호출하도록 수정합니다.
        # 사용자의 프롬프트가 AI 모델에 직접 전달되어, 의도한 대로 답변이 생성되도록 합니다.
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")

        # Google Gemini API 직접 사용
        llm = GoogleGenerativeAI(
            google_api_key=google_api_key,
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            temperature=0.7
        )
        comprehensive_report = llm.invoke(prompt)
        
        report_parts = ["💎 AI 관상 종합 분석 리포트 💎\n\n"]
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
            "FOREHEAD_WIDE_HIGH",
            "NOSE_WIDE_WINGS",
            "MOUTH_CORNERS_UP"
        ]
        print(f"\n테스트 키: {test_keys}")
        print("\n리포트를 생성합니다...\n")
        final_report = generate_report(test_keys)
        print(final_report)
