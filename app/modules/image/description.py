import base64
import re
from typing import Dict, List

from openai import OpenAI


def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def analyze_image_with_openai(
    image_path: str, client: OpenAI
) -> Dict[str, str | List[str]]:
    base64_image = encode_image_to_base64(image_path)

    prompt = """
    다음 이미지를 분석해서 사람들이 실제 검색할 때 사용할 수 있는 표현으로 설명과 태그를 생성해주세요.

    요구 사항:

    1. 설명 (description)
    - 한국어로 된 자연스럽고 구체적인 한 문장
    - 누가, 무엇을, 어디서, 어떤 모습인지 포함
    - 사람들이 자주 검색하는 표현, 줄임말(예: 증사=증명사진, 셀카, 후드, 단발, 노을샷 등)을 자연스럽게 포함
    - **이미지에 고유명사(장소명, 브랜드명, 상호명 등)가 명확히 보이면 반드시 설명에 포함해주세요**

    2. 태그 (tags)
    - 이미지의 핵심적인 속성을 나타내는 짧은 단어 3~5개
    - 아래와 같은 실제 검색어로 사용될만한 표현 사용
      예: "증사", "셀카", "후드", "단발", "노을샷", "정면", "흑백", "배경 없음", "초근접", "전신", "야외", "학교"
    - **고유명사(예: 스타벅스, 맥북, 경복궁 등)가 보일 경우 태그에도 포함**

    출력 형식 (그 외 텍스트는 절대 포함하지 마세요):

    {
      "description": "...",
      "tags": ["...", "...", "..."]
    }
    """

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{base64_image}',
                            'detail': 'high',
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
    )

    content = response.choices[0].message.content.strip()
    return parse_response_as_json(content)


def parse_response_as_json(text: str) -> Dict[str, str | List[str]]:
    description = re.search(r'"description"\s*:\s*"([^"]+)"', text)
    tags = re.findall(r'"tags"\s*:\s*\[([^\]]+)\]', text)

    tag_list = []
    if tags:
        tag_list = [
            tag.strip().strip('"\'') for tag in tags[0].split(',') if tag.strip()
        ]

    response = {
        'description': description.group(1) if description else '',
        'tags': tag_list,
    }

    print(response)

    return response
