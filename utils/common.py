


def parse_form_json(form):
    parsed_json = dict()
    for key in form.keys():
        try:
            parsed_json[key] = form[key]
        except:
            parsed_json[key] = ''

    return parsed_json
