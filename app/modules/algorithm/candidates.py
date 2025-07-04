from typing import List

from app.models import Image
from app.modules.algorithm.extract_chosung import extract_chosung, to_compat_jamo
from app.modules.algorithm.levenshtein_distance import levenshtein_distance
from app.modules.algorithm.trie import Trie


def score_match(query: str, item) -> float:
    query = query.strip().lower()
    query_chosung = extract_chosung(query)

    desc = (item.description or '').lower()
    desc_chosung = (item.description_chosung or '').lower()
    tags = [tag.lower() for tag in (item.tags or [])]
    tags_chosung = [tag.lower() for tag in (item.tags_chosung or [])]

    score = 0.0

    # 직접 매치
    if query in desc:
        score += 1.0
    if any(query == tag for tag in tags):
        score += 0.8
    if any(query in tag or tag in query for tag in tags):  # ← 추가
        score += 0.7
    if query in desc_chosung:
        score += 0.7
    if any(query == tag for tag in tags_chosung):
        score += 0.6
    if any(query in tag or tag in query for tag in tags_chosung):  # ← 추가
        score += 0.5

    if query_chosung in desc:
        score += 0.6
    if any(query_chosung == tag for tag in tags):
        score += 0.5
    if any(query_chosung in tag or tag in query_chosung for tag in tags):  # ← 추가
        score += 0.5
    if query_chosung in desc_chosung:
        score += 0.8
    if any(query_chosung == tag for tag in tags_chosung):
        score += 0.7
    if any(
        query_chosung in tag or tag in query_chosung for tag in tags_chosung
    ):  # ← 추가
        score += 0.6

    for w in desc.split() + tags:
        if levenshtein_distance(query, w) <= 2:
            score += 0.3
            break

    return score


def get_candidates(query: str, db: list, threshold: float = 0.5):
    results = []
    for item in db:
        score = score_match(query, item)
        if score >= threshold:
            results.append((item, score))
    return [item for item, _ in sorted(results, key=lambda x: -x[1])]


def get_candidates_by_queries(query_list: list[str], db: list, threshold: float = 0.5):
    final = []
    seen_ids = set()

    for q in query_list:
        for item in get_candidates(q, db, threshold=threshold):
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                final.append(item)

    return final


async def get_candidates_chosung_only(query: str) -> List:
    query = to_compat_jamo(query.lower().replace(' ', ''))

    items = await Image.all()
    desc_trie = Trie()
    tag_trie = Trie()

    for item in items:
        desc_chosung = (item.description_chosung or '').lower().replace(' ', '')
        if desc_chosung:
            desc_trie.insert(desc_chosung, item)

        for tag in item.tags_chosung or []:
            tag_chosung = (tag or '').lower().replace(' ', '')
            if tag_chosung:
                tag_trie.insert(tag_chosung, item)

    desc_matches = desc_trie.search_prefix(query)
    tag_matches = tag_trie.search_prefix(query)

    result_map = {item.id: item for item in desc_matches + tag_matches}
    return list(result_map.values())
