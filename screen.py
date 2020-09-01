import warnings
from flask import (jsonify, )
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


def res(offer_description, candidates):
    candidate_ids = [candidate["id"] for candidate in candidates]
    candidate_descriptions = [candidate["description"] for candidate in candidates]
    candidate_ids_vector = []
    candidate_descriptions_vector = []
    ordered_candidate_scores = []

    try:
        tttt = summarize(str(offer_description))
        text = [tttt]
    except Exception as e:
        print(e)
        text = [offer_description]

    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(text)
    vector = vectorizer.transform(text)

    job_desc = vector.toarray()

    for n, item in enumerate(candidate_descriptions):
        text = item
        tttt = str(text)
        try:
            tttt = summarize(tttt, word_count=100)
            text = [tttt]
            vector = vectorizer.transform(text)

            aaa = vector.toarray()
            candidate_descriptions_vector.append(vector.toarray())
            candidate_ids_vector.append(candidate_ids[n])
        except Exception as e:
            print(e)

    for i in candidate_descriptions_vector:
        samples = i
        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(samples)
        NearestNeighbors(algorithm='auto', leaf_size=30)

        ordered_candidate_scores.extend(neigh.kneighbors(job_desc)[0][0].tolist())

    z = [(y, x) for y, x in sorted(zip(ordered_candidate_scores, candidate_ids_vector))]

    results = {
        "scores": [],
        "candidates": []
    }

    for item in z:
        results["scores"] = [item[0]] + results["scores"]
        results["candidates"] = [item[1]] + results["candidates"]

    return results


if __name__ == '__main__':
    inputStr = input("")
