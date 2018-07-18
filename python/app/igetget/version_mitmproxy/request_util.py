import json
import base64
import time
import random
import requests
from urllib.parse import urlparse, urlencode
import igetget_config
import lsieun_util


def get_raw_headers() -> dict:
    file_path = igetget_config.IGETGET_HEADERS_PATH
    line_list = lsieun_util.read_line_list(file_path)
    json_str = line_list[0]

    headers = json.loads(json_str)
    return headers


def update_headers(headers: dict, content_type: str, timestamp: str, nonce: str, sign: str) -> None:
    """
    更新Request的headers

    :param headers:
    :param content_type: application/x-www-form-urlencoded 或
    :param timestamp:
    :param nonce:
    :param sign:
    :return:
    """
    headers["Content-Type"] = content_type
    headers["G-Auth-Ts"] = timestamp
    headers["G-Auth-Nonce"] = nonce
    headers["G-Auth-Sign"] = sign


def current_timestamp():
    t = time.time()
    seconds = int(round(t))
    return str(seconds)


def get_random_char():
    char_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    index = random.randint(0, len(char_list)-1)
    return char_list[index]


def get_nonce(count = 16):
    nonce = ""

    num = 0
    while num < count:
        ch = get_random_char()
        nonce += ch
        num = num + 1

    return nonce


def generate_sign(encoded_path: str, method: str,
                  encoded_query: str, content_type: str,
                  payload: str, timestamp: str,
                  nonce: str, token: str, verbose=True):
    """
    encoded_path = "/parthenon/v1/articleaudio/listall"
    method = "POST"
    encoded_query = ""
    content_type = "application/x-www-form-urlencoded"
    body_param = "column_id=20&count=20&max_id=0&order=1&section=0&since_id=0"
    timestamp = "1531555906"
    nonce = "3ebcd8a61e161b4c"
    token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsdW9qaWxhYi5jb20iLCJleHAiOjE1MzI4NTE4ODUsImlhdCI6MTUzMTU1NTg4NSwiaXNzIjoiRWFzZUdhdGV3YXkgSldUQXV0aCBQbHVnaW4iLCJuYmYiOjE1MzE1NTU4ODUsInN1YiI6IjE5MDcyNDgifQ.9baS3uzV_YnO7HxdfrG7IoQtppWA8K398lare2mUVsupqUtQ6OX4rI6QtkxqMgCoNYvpD1vKOQKVOLIKDyQlxg"
    """
    # 拼接字符串
    conn_str = ""
    conn_str = conn_str + encoded_path + "\n"
    conn_str = conn_str + method + "\n"
    conn_str = conn_str + encoded_query + "\n"
    conn_str = conn_str + content_type + "\n"
    conn_str = conn_str + payload + "\n"
    conn_str = conn_str + timestamp + "\n"
    conn_str = conn_str + nonce + "\n"
    conn_str = conn_str + token

    # MD5加密
    # m = hashlib.md5()
    # m.update(conn_str.encode("UTF8"))
    # md5_str = m.hexdigest()
    md5_str = lsieun_util.make_md5(conn_str)
    md5_bytes = md5_str.encode("UTF8")

    # Base64编码
    base64_bytes = base64.b64encode(md5_bytes)
    base64_str = base64_bytes.decode("UTF8")

    if verbose:
        print("="*30, "sign", "="*30)
        print("  conn_str = \r\n%s" % conn_str)
        print("   md5_str = %s" % md5_str)
        print("base64_str = %s" % base64_str)
        print("=" * 66)

    return base64_str


def post(url: str, post_data: dict, content_type: str, verbose=True) -> str:
    # （1）請求的url和data
    parse_result = urlparse(url)
    encoded_path = parse_result.path
    encoded_query = parse_result.query
    if content_type == igetget_config.CONTENT_TYPE_JSON:
        payload = json.dumps(post_data)
    else:
        payload = urlencode(post_data)

    if verbose:
        print("="*30, "post", "="*30)
        print("url = {}".format(url))
        print("encoded_path = {}".format(encoded_path))
        print("encoded_query = {}".format(encoded_query))
        print("payload = {}".format(payload))
        print("=" * 66)

    # （2）請求headers
    headers = get_raw_headers()
    token = headers.get("G-Auth-Token")
    method = igetget_config.METHOD_POST
    timestamp = current_timestamp()
    nonce = get_nonce()
    sign = generate_sign(encoded_path, method, encoded_query, content_type, payload, timestamp, nonce, token)
    update_headers(headers, content_type, timestamp, nonce, sign)

    if verbose:
        lsieun_util.view(headers, "Request Headers")

    # （3）發送請求，返回數據
    r = requests.post(url, data=payload.encode("UTF8"), headers=headers)
    status_code = r.status_code
    response_headers = r.headers
    response_text = r.text
    if verbose:
        print("status_code = {}".format(status_code))
        print("response_headers = {}".format(response_headers))
        print("response_text = {}".format(response_text))
        print("=" * 60)

    return response_text


def get_data_list(response_text: str) -> list:
    d = json.loads(response_text)
    c = d.get("c")
    lst = c.get("list")
    return lst
