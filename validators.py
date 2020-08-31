def has_params(request, required_params):
    if not request:
        return 400, "Request is empty"

    for param in required_params:
        if param not in request:
            return 400, "Parameter missing"

    return 200, "Success"


def is_param_empty(param):
    if len(param) == 0:
        return True
    else:
        return False


def candidate_has_format(candidate, index):
    if 'id' not in candidate:
        return 400, "ID missing in candidate [{}]".format(str(index))

    if 'description' not in candidate:
        return 400, "description missing in candidate [{}]".format(str(index))

    if not isinstance(candidate['id'], str):
        return 400, "ID is not a string in candidate [{}]".format(str(index))

    if not isinstance(candidate['description'], str):
        return 400, "Description is not a string in candidate [{}]".format(str(index))

    return 200, "Success"


def validate_candidates(candidates):
    for index, candidate in enumerate(candidates):
        code, msg = candidate_has_format(candidate, index)

        if code == 400:
            return code, msg

    return 200, "Success"


def run_param_validators(text, candidates):
    if is_param_empty(text) or is_param_empty(candidates):
        return 400, "Empty parameter"

    return validate_candidates(candidates)
