import json
import requests
import igetget_config
import lsieun_util


def get_flow_list(host: str, port: int, verbose: bool=False):
    """
    获取mitmweb的flows

    :param host: mitmweb的主机IP地址
    :param port: mitmweb在Web Server的端口号
    :param verbose: 是否打印日志
    :return: mitmweb的flows
    """
    template = "http://{host}:{port}/flows.json"
    url = template.format(host=host, port=port)

    r = requests.get(url)
    flows_text = r.text
    if verbose:
        print("url:", url)
        print("status code:", r.status_code)
        print("headers:", r.headers)
        print("flows text:", r.text)

    flow_list = json.loads(flows_text)
    return flow_list


def get_request_list(flow_list: list) -> list:
    """
    将flow list转换为request list。在mitmproxy中，flow是对request和response的总称，这个功能只获取request。

    :param flow_list: flow的列表
    :return: request的列表
    """
    req_list = []
    for flow in flow_list:
        request = flow.get("request")
        req_list.append(request)
    return req_list


def filter_req(req: dict, host_filter: str="", path_filter: str="") -> bool:
    """
    根据host(域名)和path（路径）来对request进行过滤

    :param req: http request
    :param host_filter: 域名中包含的关键字
    :param path_filter: 路径中包含的关键字
    :return: True表示符合条件，False表示不符合条件
    """
    if host_filter:
        host = req.get("host")
        if host.find(host_filter) < 0:
            return False

    if path_filter:
        path = req.get("path")
        if path.find(path_filter) < 0:
            return False

    return True


def filter_requests(req_list: list, host_filter: str="", path_filter: str="") -> list:
    """
    过滤request的列表

    :param req_list:
    :param host_filter:
    :param path_filter:
    :return:
    """
    new_list = []

    for req in req_list:
        is_ok = filter_req(req, host_filter, path_filter)
        if is_ok:
            new_list.append(req)

    return new_list


def get_latest_request_by_header_key(req_list: list, header_key: str) -> dict:
    """
    从request list中获取包含指定header key的最新的request

    :param req_list:
    :param header_key:
    :return:
    """
    target_req = None

    for req in req_list:
        header_list = req.get("headers")
        for header in header_list:
            if header[0] == header_key:
                target_req = req

    return target_req


def get_header_dict(req: dict) -> dict:
    """
    这是一个特殊的方法，它是由于mitmweb中req的格式特殊性造成的。
    平常的request中，headers是一个dict格式，而在mitmweb中，header是一个数组。
    这里就是将”数组格式“的header转换成”dict格式“的headers。

    :param req:
    :return:
    """
    header_dict = {}
    header_list = req.get("headers")
    for header in header_list:
        k = header[0]
        v = header[1]
        header_dict[k] = v
    return header_dict


def get_statistic_dict(req_list: list) -> dict:
    stat_dic = {}

    for req in req_list:
        path = req.get("path")
        if path.find(".jpg") > 0 or path.find(".png") > 0:
            continue
        if path.find(".js") > 0 or path.find(".css") > 0:
            continue

        if path.find("?") > 0:
            end_index = path.find("?")
            path = path[:end_index]

        num = stat_dic.get(path, 0)
        stat_dic[path] = num + 1

    return stat_dic


def save_igetget_headers(host, port):
    # （1）獲取mitmweb中的所有flow
    flow_list = get_flow_list(host, port)
    # （2）獲取所有request
    all_req_list = get_request_list(flow_list)
    # （3）過濾出所有“得到App”的請求
    req_list = filter_requests(all_req_list, host_filter="igetget.com")
    # （4）獲取最新的一個request
    latest_req = get_latest_request_by_header_key(req_list, "G-Auth-Token")
    # （5）從request中提取headers
    header_dict = get_header_dict(latest_req)
    lsieun_util.view(header_dict)
    # （6）將headers寫入文件中
    lsieun_util.write(header_dict, igetget_config.IGETGET_HEADERS_PATH)

    # （7）獲取URL訪問次數
    stat_dict = get_statistic_dict(req_list)
    lsieun_util.view_dict_by_value(stat_dict)


if __name__ == '__main__':
    server_ip = igetget_config.MITMWEB_HOST
    server_port = igetget_config.MITMWEB_PORT

    # igetget
    save_igetget_headers(host=server_ip, port=server_port)


