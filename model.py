from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def filter_texts(texts, keyword, threshold):
    combined = [keyword] + texts
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(combined)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    result = []
    for i, score in enumerate(sims):
        if score >= threshold:
            result.append({'text': texts[i], 'score': float(score)})
    return result
