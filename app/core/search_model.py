from sentence_transformers import SentenceTransformer

_model = None


def get_search_model():
    global _model
    if _model is None:
        print('[INFO] 의미 기반 한국어 SBERT 모델 로드 중...')
        _model = SentenceTransformer('jhgan/ko-sbert-nli')
    return _model
