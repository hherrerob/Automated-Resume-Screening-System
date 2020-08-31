import warnings
import screen
import search
import utils
import validators

from flask import (Flask, request)
from flask_cors import CORS

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)
CORS(app)

app.config.from_object(__name__)


@app.route('/candidate/compare', methods=['POST'])
def candidate_compare():
    code, msg = validators.has_params(request.json, ['offer', 'candidates'])

    if code == 400:
        return utils.make_response(code, msg)

    offer = request.json['offer']
    candidates = request.json['candidates']

    code, msg = validators.run_param_validators(offer, candidates)

    if code == 400:
        return utils.make_response(code, msg)

    try:
        results = screen.res(offer, candidates)
        return utils.make_response(200, results)
    except Exception as e:
        return utils.make_response(500, str(e))


@app.route('/candidate/search', methods=['POST'])
def candidate_search():
    code, msg = validators.has_params(request.json, ['search', 'candidates'])

    if code == 400:
        return utils.make_response(code, msg)

    search_text = request.json['search']
    candidates = request.json['candidates']

    print(candidates)

    code, msg = validators.run_param_validators(search_text, candidates)

    if code == 400:
        return utils.make_response(code, msg)

    try:
        results = search.res(search_text, candidates)
        return utils.make_response(200, results)
    except Exception as e:
        return utils.make_response(500, str(e))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True, threaded=True)
