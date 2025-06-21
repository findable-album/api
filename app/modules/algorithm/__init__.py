from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.openai_client import get_openai_client
from app.core.search_model import get_search_model
from app.models import Image
from app.modules.algorithm.candidates import (
    get_candidates_by_queries,
    get_candidates_chosung_only,
)
from app.modules.algorithm.extract_chosung import is_chosung_query
from app.modules.algorithm.rewrite_query import dynamic_query_rewrite


def build_search_text(item) -> str:
    return f'설명: {item.description or ""}. 태그: {" ".join(item.tags or [])}'


def rerank_with_bert(query: str, candidates: list, model: SentenceTransformer):
    if not candidates:
        return []

    search_texts = [build_search_text(item) for item in candidates]
    desc_embs = model.encode(search_texts)
    query_emb = model.encode([query])
    sims = cosine_similarity(query_emb, desc_embs)[0]

    return sorted(
        [(item, float(sim)) for item, sim in zip(candidates, sims)], key=lambda x: -x[1]
    )


async def search_images(query: str):
    client = get_openai_client()

    model = get_search_model()

    if is_chosung_query(query):
        candidates = await get_candidates_chosung_only(query)
        return candidates
    else:
        image_db = await Image.all()

        rewritten_query = dynamic_query_rewrite(query, client)
        queries = [query, rewritten_query] if rewritten_query else [query]

    candidates = get_candidates_by_queries(queries, image_db)

    if not is_chosung_query(query):
        model = get_search_model()
        candidates = rerank_with_bert(query, candidates, model)

    return candidates
