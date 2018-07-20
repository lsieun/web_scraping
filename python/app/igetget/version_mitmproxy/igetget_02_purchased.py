import json
import igetget_config
import request_util
import lsieun_util
import igetget_parthenon
import igetget_article


def get_purchased_structure() -> list:
    url = "https://entree.igetget.com/purchased/v1/index/structure"
    post_data = {}
    response_text = request_util.post(url, post_data, igetget_config.CONTENT_TYPE_FORM)
    lst = request_util.get_data_list(response_text)
    lsieun_util.view(lst)
    return lst


def get_group_data(group_type: int, order_name: str) -> list:
    # （1）請求的url和data
    url = "https://entree.igetget.com/purchased/v1/index/groupdata"
    post_data = {
        "group_type" : group_type,
        "order_name" : order_name
    }

    response_text = request_util.post(url, post_data, igetget_config.CONTENT_TYPE_FORM)
    lst = request_util.get_data_list(response_text)
    lsieun_util.view(lst)
    return lst






def get_purchased_column():
    column_list = get_group_data(4, "open")

    column_id_list = []
    for column in column_list:
        column_id = column.get("id")
        title = column.get("title")
        column_id_list.append(column_id)
        lsieun_util.view(column)
        igetget_parthenon.get_article_list(column_id)
        igetget_article.create_column_index(column_id)
        igetget_article.save_article_content(column_id)
        igetget_article.write_single_html(column_id)


if __name__ == '__main__':
    get_purchased_structure()
    get_purchased_column()

    # get_category_list(40)
