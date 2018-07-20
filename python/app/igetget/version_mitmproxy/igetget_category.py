import json
import igetget_config
import lsieun_util
import request_util


def save_category_list(group_type):
    url = "https://entree.igetget.com/purchased/v1/category/lists"

    category_list = []
    page = 1
    while True:
        post_data = {
            "group_type": group_type,
            "order_name": "open",
            "page": page
        }

        response_text = request_util.post(url, post_data, igetget_config.CONTENT_TYPE_FORM)
        lst = request_util.get_data_list(response_text)
        if len(lst) < 1: break
        category_list.append(response_text)
        page += 1

    template = igetget_config.IGETGET_CATEGORY_PATH
    file_path = template.format(group_type)
    lsieun_util.write(category_list, file_path)


def simplify_course_category(category):
    category_id = category.get("id")
    title = category.get("title")
    type = category.get("type")
    desc = category.get("desc")
    course_num = category.get("course_num")
    create_time = category.get("create_time")

    return (category_id, title, desc)


def get_course_category(group_type = 40):
    template = igetget_config.IGETGET_CATEGORY_PATH
    file_path = template.format(group_type)

    category_list = []
    line_list = lsieun_util.read_line_list(file_path)
    for line in line_list:
        lst = request_util.get_data_list(line)
        category_list += lst

    cat_list = []
    for category in category_list:
        cat = simplify_course_category(category)
        cat_list.append(cat)

    lsieun_util.view(cat_list)

    return cat_list


if __name__ == '__main__':
    # 保存全部课程的目录
    # course_group_type = 40
    # save_category_list(course_group_type)

    get_course_category()