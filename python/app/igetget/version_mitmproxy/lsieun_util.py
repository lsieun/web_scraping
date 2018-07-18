import hashlib
import json
import os
import time


def current_milliseconds():
    t = time.time()
    seconds = int(round(t))
    return str(seconds)


def view_dict(d: dict) -> None:
    for k,v in sorted(d.items()):
        print("%s: %s" % (k,v))


def view_dict_by_value(d: dict) -> None:
    lst = [ (k,v) for k, v in d.items()]
    for k, v in sorted(lst, key= lambda x:x[1], reverse=True):
        print("%s: %s" % (k, v))


def view_type(o: object) -> None:
    print(type(o))


def view_set(s: set) -> None:
    for item in sorted(s):
        print(item)


def view_list(lst: list) -> None:
    for item in lst:
        print(item)


def view(o: object, display_name="object") -> None:
    if o is None:
        print("object is None")
        return

    t = type(o)
    print("="*20, "type({})={}".format(display_name, t), "="*20)
    if t is dict:
        view_dict(o)
    elif t is list:
        view_list(o)
    elif t is set:
        view_set(o)
    else:
        print("There is something Wrong!!!")
    print("="*66)


def walk_dir(dir_path: str, verbose: bool=False) -> tuple:
    count = 0
    file_path_list = []

    for parent, dirnames, file_name_list in os.walk(dir_path):
        for file_name in file_name_list:
            file_path = os.path.join(parent, file_name)
            file_path_list.append(file_path)
            count += 1

            if verbose:
                print('文件名：%s' % file_name)
                print('文件完整路径：%s\r\n' % file_path)
    if verbose:
        print("total count = %s" % count)
        print("="*120)

    return count, file_path_list


def filter_path(file_path_list: list, path_filter: str="", content_filter: str="") -> set:
    path_set = set()
    for file_path in file_path_list:
        if path_filter:
            if file_path.find(path_filter) < 0:
                continue

        if content_filter:
            with open(file_path, "rb") as f:
                for line in f.readlines():
                    try:
                        line = line.decode("UTF8")
                    except Exception as ex:
                        break
                    line = line.strip()
                    if line.find(content_filter) > -1:
                        path_set.add(file_path)
                        break
        else:
            path_set.add(file_path)

    return path_set


def find_file(dir_path: str, path_filter: str="", content_filter: str="") -> None:
    count, file_path_list = walk_dir(dir_path)
    print("total file count: %s" % count)
    path_set = filter_path(file_path_list, path_filter, content_filter)
    print("="*120)
    view_set(path_set)


def read_line_list(file_path: str, encoding: str="UTF-8") -> list:
    line_list = []
    with open(file_path, "rb") as f:
        for line in f.readlines():
            line = line.decode(encoding)
            if not line: continue
            line_list.append(line)
    return line_list


def prepare_write(file_path: str) -> None:
    dir_path = os.path.abspath(os.path.join(file_path, os.pardir))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def write_line_list(line_list: list, file_path: str, encoding="UTF-8") -> None:
    prepare_write(file_path)

    with open(file_path, "wb") as f:
        for line in line_list:
            if line is None: continue
            line = line + "\r\n"
            data = line.encode(encoding)
            f.write(data)


def write_dict(d: dict, file_path: str, encoding="UTF-8") -> None:
    prepare_write(file_path)

    json_str = json.dumps(d)
    write_str(json_str, file_path, encoding)


def write_str(s: str, file_path: str, encoding="UTF-8") -> None:
    prepare_write(file_path)

    with open(file_path, "wb") as f:
        data = s.encode(encoding)
        f.write(data)


def write(o: object, file_path: str, verbose=True) -> None:
    if o is None: return

    is_ok = True
    t = type(o)
    if t is list:
        write_line_list(o, file_path)
    elif t is dict:
        write_dict(o, file_path)
    elif t is str:
        write_str(o, file_path)
    else:
        is_ok = False
        print("There is something Wrong!!!")

    if verbose:
        print("="*27,"write file", "="*27)
        if is_ok:
            template = "Write File Success: {}"
        else:
            template = "Wow, Wow, Wow!!! Write File Failed: {}"
        result = template.format(file_path)
        print(result)
        print("="*66)


def make_md5(val: str, encoding="UTF-8") -> str:
    m = hashlib.md5()
    m.update(val.encode(encoding))
    md5_str = m.hexdigest()
    return md5_str

if __name__ == '__main__':
    # find_file("D:\liusen\git_repo\web_scraping", path_filter=".py", content_filter="argparse")
    find_file("D:\liusen\git_repo\learn-spider\python", path_filter=".md", content_filter="os.path.exist")