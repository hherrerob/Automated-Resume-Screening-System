import re
import unicodedata
import nltk
import inflect
import warnings

from flask import (Flask)
from autocorrect import spell
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        # print(word)
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas


def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    words = stem_words(words)
    words = lemmatize_verbs(words)
    return words


def spell_correct(to_correct):
    words = to_correct.split(" ")
    correct_words = []
    for i in words:
        correct_words.append(spell(i))
    return " ".join(correct_words)


def lcs(x, y):
    try:
        mat = []
        for i in range(0, len(x)):
            row = []
            for j in range(0, len(y)):
                if x[i] == y[j]:
                    if i == 0 or j == 0:
                        row.append(1)
                    else:
                        val = 1 + int(mat[i - 1][j - 1])
                        row.append(val)
                else:
                    row.append(0)
            mat.append(row)
        new_mat = []
        for r in mat:
            r.sort()
            r.reverse()
            new_mat.append(r)
        _lcs = 0
        for r in new_mat:
            if _lcs < r[0]:
                _lcs = r[0]

        return _lcs
    except Exception as e:
        print(e)
        return -9999


def res(search_text, candidates):
    final_array = []

    def semantic_search(search_string, search_sentences_list):
        result = None
        search_string = spell_correct(search_string)
        best_score = 0
        for i in search_sentences_list:
            score = lcs(search_string, i)
            temp = [score]
            final_array.extend(temp)
            if score > best_score:
                best_score = score
                result = i

        return result

    candidate_ids = [candidate["id"] for candidate in candidates]
    candidate_descriptions = [candidate["description"] for candidate in candidates]

    for m, i in enumerate(candidate_descriptions):
        candidate_descriptions[m] = nltk.word_tokenize(candidate_descriptions[m])
        candidate_descriptions[m] = normalize(candidate_descriptions[m])
        candidate_descriptions[m] = ' '.join(map(str, candidate_descriptions[m]))

    search_text = nltk.word_tokenize(search_text)
    search_text = normalize(search_text)
    search_text = ' '.join(map(str, search_text))

    semantic_search(search_text, candidate_descriptions)

    z = [(y, x) for y, x in sorted(zip(final_array, candidate_ids), reverse=True)]

    results = {
        "scores": [],
        "candidates": []
    }

    for item in z:
        results["scores"].append(item[0])
        results["candidates"].append(item[1])

    return results

