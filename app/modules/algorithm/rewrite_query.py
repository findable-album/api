from openai import OpenAI


def dynamic_query_rewrite(query, client: OpenAI):
    prompt = f"""
    사용자의 검색어를 더 명확하고 의미가 풍부하게 다시 표현해줘.

    - 고유명사(브랜드명, 장소명, 인명 등)는 절대 변경하지 말고 그대로 유지해줘.
    - 단어의 의미가 풍부해지도록 자연스러운 문장으로 바꿔줘.
    - 검색 상황에 어울리는 묘사나 분위기를 추가해도 좋아.
    - 출력은 한 문장, 따옴표 없이.

    예시:
    - "증명사진" → "정면을 응시한 깔끔한 배경의 인물 사진"
    - "따뜻한 분위기" → "따뜻한 조명과 감성적인 느낌의 이미지"
    - "스타벅스" → "스타벅스 매장 내부에서 찍은 일상적인 장면"

    검색어: "{query}"
    출력:
    """

    response = client.chat.completions.create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=50,
        temperature=0.5,
    )

    result = response.choices[0].message.content.strip().strip('"')

    if not result:
        return query.strip()

    return f'{query.strip()}: {result.strip()}'.strip()
