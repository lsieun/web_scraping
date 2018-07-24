import json
import requests
import geekbang_util


def post_json(url: str, payload:dict ={}, headers:dict =None, verbose=True):
    json_str = json.dumps(payload)
    if headers is None:
        headers = geekbang_util.get_headers()
    r = requests.post(url, data=json_str, headers=headers)
    status_code = r.status_code
    headers = r.headers
    resp_text = r.text
    if verbose:
        print("url: ", url)
        print("status code: ", status_code)
        print("headers: ", headers)
        print("reponse text: ", resp_text)

    return resp_text

