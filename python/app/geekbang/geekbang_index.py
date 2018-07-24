import geekbang_article
import geekbang_column_articles
import geekbang_columns
import geekbang_util
import json


if __name__ == '__main__':
    my_text = geekbang_columns.get_my_columns()
    d = json.loads(my_text)
    data = d.get("data")
    lst = data.get("list")
    for c in lst:
        column_id = c.get("id")
        geekbang_column_articles.process(column_id)
        geekbang_article.process(column_id)
    print("OVER")
