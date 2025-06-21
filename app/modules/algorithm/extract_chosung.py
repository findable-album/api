import re


def extract_chosung(text):
    result = ''
    for char in text:
        if '가' <= char <= '힣':
            code = ord(char) - ord('가')
            choseong_index = code // (21 * 28)
            choseong = chr(0x1100 + choseong_index)
            result += choseong
        else:
            result += char
    return result


def is_chosung_query(query: str) -> bool:
    return bool(re.fullmatch(r'[ㄱ-ㅎ]+', query.strip()))


def to_compat_jamo(text: str) -> str:
    compat_map = {
        'ㄱ': 'ᄀ',
        'ㄲ': 'ᄁ',
        'ㄴ': 'ᄂ',
        'ㄷ': 'ᄃ',
        'ㄸ': 'ᄄ',
        'ㄹ': 'ᄅ',
        'ㅁ': 'ᄆ',
        'ㅂ': 'ᄇ',
        'ㅃ': 'ᄈ',
        'ㅅ': 'ᄉ',
        'ㅆ': 'ᄊ',
        'ㅇ': 'ᄋ',
        'ㅈ': 'ᄌ',
        'ㅉ': 'ᄍ',
        'ㅊ': 'ᄎ',
        'ㅋ': 'ᄏ',
        'ㅌ': 'ᄐ',
        'ㅍ': 'ᄑ',
        'ㅎ': 'ᄒ',
    }

    result = []
    for ch in text:
        result.append(compat_map.get(ch, ch))
    return ''.join(result)
