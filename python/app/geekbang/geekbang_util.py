import json
import os


def get_headers() -> dict:
    headers = {
        "Host": "time.geekbang.org",
        "X-GEEK-APP-NAME": "time",
        "X-GEEK-DEVICE-MODEL": "iPhone7,1",
        "Accept": "*/*",
        "X-GEEK-OS-VER": "11.4",
        "Ticket": "BAkBAQwBAQIE70ZKWwQEIBwAAAsCBAADBEdEVVsKBAIAAAABBHI0EAAFBIDGEwAHBP6gC88IAQEGBPF_j.4-",
        "X-GEEK-VER-NAME": "1.1.6",
        "Device-Id": "C55825C4-786E-4117-BF9A-DD6C298DD880",
        "Device-Token": "0467b3892e2d6fab771393920d99f563e701ade4ad8f0fbb984eb06a58b399de",
        "Accept-Language": "en-us",
        "Accept-Encoding": "br, gzip, deflate",
        "Content-Type": "application/json",
        "Content-Length": "2",
        "User-Agent": "iPhone7,1(iOS/11.4) GeekbangApp(Zeus/1.1.6) Weex/0.16.1 ExternalUA 1125x2001",
        "X-GEEK-OS-PLATFORM": "iOS",
        "Referer": "http://www.geekbang.org/",
        "X-GEEK-OS-NAME": "iOS",
        "Connection": "keep-alive",
        "Cookie": "SERVERID=fe79ab1762e8fabea8cbf989406ba8f4|1532314814|1532314696; GCESS=BAkBAQwBAQIE70ZKWwQEIBwAAAsCBAADBEdEVVsKBAIAAAABBHI0EAAFBIDGEwAHBP6gC88IAQEGBPF_j.4-; GCID=C55825C4-786E-4117-BF9A-DD6C298DD880; _ga=GA1.2.987119294.1520329997"
    }
    return headers


def view_dict(d: dict) -> None:
    for k, v in sorted(d.items()):
        print("%s: %s" % (k,v))


def view_list(lst: list) -> None:
    for item in lst:
        print(item)


def view_set(s: set) -> None:
    for item in sorted(s):
        print(item)


def view(o:object) -> None:
    if o is None: return
    t = type(o)
    print("type(object) = %s" % t)
    if t == dict:
        view_dict(o)
    elif t == list:
        view_list(o)
    elif t == set:
        view_set(o)
    elif t == tuple:
        print(o)
    elif t == str:
        print(o)
    else:
        print("There is Something Wrong!!!")


def read_line_list(file_path: str, encoding="UTF8") -> list:
    line_list = list()
    with open(file_path, "rb") as f:
        for line in f.readlines():
            line = line.decode(encoding)
            line_list.append(line)
    return line_list


def prepare_write(file_path: str) -> None:
    dir_path = os.path.abspath(os.path.join(file_path, os.pardir))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def write_list(line_list: list, file_path, encoding="UTF8") -> None:
    prepare_write(file_path)
    with open(file_path, "wb") as f:
        for line in line_list:
            line += "\r\n"
            data = line.encode(encoding)
            f.write(data)


def write_str(s: str, file_path: str, encoding="UTF8") -> None:
    prepare_write(file_path)
    with open(file_path, "wb") as f:
        data = bytes(s, encoding=encoding)
        f.write(data)


def write_dict(d: dict, file_path: str, encoding="UTF8") -> None:
    prepare_write(file_path)
    json_str = json.dumps(d)
    write_str(json_str, file_path, encoding)


def write(o: object, file_path: str, encoding="UTF8") -> None:
    if o is None: return
    t = type(o)

    is_ok = True
    if t == list:
        write_list(o, file_path)
    elif t == dict:
        write_dict(o, file_path)
    elif t == str:
        write_str(o, file_path)
    else:
        is_ok = False

    if is_ok:
        print("Write File Success: %s" % file_path)
    else:
        print("Write File Failed!!! File Name: %s" % file_path)


