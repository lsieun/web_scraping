import time
import igetget_config
import request_util
import lsieun_util


def get_post_data(column_id: int, max_id: str) -> dict:
    data = {
        "column_id": column_id,
        "count": "20",
        "max_id": max_id,
        "order": "1",
        "section": "0",
        "since_id": "0"
    }
    return data


def get_info(response_text):
    # resp_dict = json.loads(response_text)
    # content_dict = resp_dict.get("c")
    # article_list = content_dict.get("list")
    article_list = request_util.get_data_list(response_text)
    if not article_list:
        return False, None

    num = len(article_list)
    cur_article = article_list[num-1]
    publish_time_stamp = cur_article.get("publish_time_stamp")
    return True, publish_time_stamp


def get_article_list(column_id, sleep_seconds=3):
    url = "https://entree.igetget.com/parthenon/v1/articleaudio/listall"
    max_id = "0"

    resp_list = []
    index = 0
    while True:
        post_data = get_post_data(column_id, max_id)
        response_text = request_util.post(url, post_data, igetget_config.CONTENT_TYPE_FORM)
        resp_list.append(response_text)

        index = index + 1
        can_continue, max_id = get_info(response_text)
        print("%s, %s, %s" % (index, can_continue, max_id))
        if not can_continue:
            break

        time.sleep(sleep_seconds)

    template = igetget_config.IGETGET_COLUMNS_PATH
    file_path = template.format(column_id)
    lsieun_util.write(resp_list, file_path)
    # with open(file_path, "wb") as f:
    #     for line in resp_list:
    #         line = line + "\r\n"
    #         data = line.encode("UTF8")
    #         f.write(data)


if __name__ == '__main__':
    # get_article_list(20)
    # get_article_list(36)
    get_article_list(46)